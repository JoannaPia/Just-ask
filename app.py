from flask import Flask, render_template, request, url_for, redirect
import os
import data_manager
import re


HEADERS_PRINT = {"id": "Question ID", "submission_time": "Submission time", "view_number": "View number",
                 "vote_number": "Vote number", "title": "Title", "message": "Message", "image": "Image"}
QUESTIONS_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWERS_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
TARGET_FOLDER = 'static/images/'
UPLOAD_FOLDER = os.path.join(APP_ROOT, TARGET_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    questions = data_manager.get_five_questions()
    comments_q = data_manager.get_comments_q()
    return render_template("index.html", headers=QUESTIONS_HEADERS, headers_print=HEADERS_PRINT, questions=questions, comments_q=comments_q)


@app.route('/list')
def list():
    questions = data_manager.get_all_questions()
    #comments_q = data_manager.get_comments_q(question_id)
    return render_template("list.html", headers=QUESTIONS_HEADERS, headers_print=HEADERS_PRINT, questions=questions)


@app.route('/add-question')
def add_question():
    return render_template('add_question.html')


@app.route('/save', methods=['POST'])
def save_question():
    title = request.form['title']
    message = request.form['message']
    id = data_manager.add_question(data_manager.data_time_now(), '0', '0', title, message, str(0))
    return redirect(url_for('display_question', question_id=id))


@app.route('/<int:question_id>/', methods=['GET'])
def display_question(question_id):
    question = data_manager.get_question(question_id)
    answers = data_manager.get_answers(question_id)
    comments = data_manager.get_comments(question_id)
    return render_template("display_question.html", headers=QUESTIONS_HEADERS, question=question,
                           answers_headers=ANSWERS_HEADERS, answers=answers, headers_print=HEADERS_PRINT,
                           comments=comments)

@app.route('/save_answer/<int:q_id>', methods=['POST'])
def save_answer(q_id):
    message = request.form['message']
    data_manager.add_answer(data_manager.data_time_now(), '0', q_id, message, str(0))
    return redirect(url_for('display_question', question_id=q_id))

@app.route('/<int:question_id>/new-answer')
def add_answer(question_id):
    return render_template('add_answer.html', question_id=question_id)


@app.route('/delete_question/<int:question_id>/')
def delete_question(question_id):
    answers_id = data_manager.get_answers_id(question_id)
    for id in answers_id:
        data_manager.delete_comment_to_answer(id["id"])
    data_manager.delete_question_tag(question_id)
    data_manager.delete_question(question_id)
    return redirect(url_for('index'))

@app.route('/answer/<int:answer_id>/delete')
def delete_comment_to_answer(answer_id):
    question_id = data_manager.delete_comment_to_answer(answer_id)
    return redirect(url_for('display_question', question_id=question_id))

@app.route('/<int:answer_id>/vote-up')
def vote_up_answers(answer_id):
    question_id = data_manager.vote_up_answer(answer_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/<int:answer_id>/vote-down')
def vote_down_answers(answer_id):
    question_id = data_manager.vote_up_answer(answer_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/<int:answer_id>/save-comment', methods=['POST'])
def save_comment_answer(answer_id):
    message = request.form['message']
    q_id = data_manager.save_comment_answer(answer_id, message)
    return redirect(url_for('display_question', question_id=q_id))

@app.route('/<int:question_id>/save-comment_q', methods=['POST'])
def save_comment_question(question_id):
    message = request.form['message']
    q_id = data_manager.save_comment_answer(question_id, message)
    return redirect(url_for('index', question_id=q_id))

@app.route('/<int:answer_id>/comment/<int:comment_id>/delete')
def delete_one_comment(comment_id, answer_id):
    q_id = data_manager.delete_one_comment(comment_id, answer_id)
    return redirect(url_for('display_question', question_id=q_id))


@app.route('/<int:question_id>/comment/<int:comment_q_id>/del')
def delete_one_comment_q(comment_q_id, question_id):
    q_id = data_manager.delete_one_comment_q(comment_q_id, question_id)
    return redirect(url_for('index', question_id=q_id))


@app.route('/answer/<int:answer_id>/edit', methods=['GET'])
def edit_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    #print(answer['message'])
    return render_template('edit_answer.html', question_id=answer['question_id'],
                           answer_id=answer_id, answer=answer)

@app.route('/answer/<int:answer_id>/save_edit_answer', methods=['POST'])
def save_edit_answer(answer_id):
    message = request.form['message']
    q_id = data_manager.save_edit_answer(answer_id, message)
    return redirect(url_for('display_question', question_id=q_id))

@app.route('/<int:answer_id>/vote-down')
def upload_image_answer(answer_id, question_id):
    pass

@app.route('/vote-up/<int:question_id>/<table>')
def vote_up_on_question(question_id, table):
    if table == "question":
        data_manager.vote_up_question(id=question_id)
    questions = data_manager.get_all_questions()
    return redirect(url_for('index'))


@app.route('/vote-down/<int:question_id>/<table>')
def vote_down_on_question(question_id, table):
    if table == "question":
        data_manager.vote_down_question(id=question_id)
    questions = data_manager.get_all_questions()
    return redirect(url_for('index'))


@app.route('/edit_question/<int:question_id>/edit', methods=['GET'])
def edit_question(question_id):
    question = data_manager.get_question(question_id)
    return render_template('edit_question.html', question_id=question['id'],
                           question=question)

@app.route('/edit_question/<int:question_id>/edit', methods=['POST'])
def save_edited_question(question_id):
    title = request.form['title']
    message = request.form['message']
    question_id = question_id
    data_manager.save_edit_question(question_id, message, title)

    return redirect(url_for('display_question', question_id=question_id))

@app.route("/search/", methods=["GET", "POST"])
def search_phrase():
    if request.method == 'POST':
        search_phrase = request.form['search_phrase']
        search_question = data_manager.search(search_phrase)
        answers = data_manager.get_all_answers()
    return render_template("search_questions.html", headers=QUESTIONS_HEADERS, headers_print=HEADERS_PRINT,
                           questions=search_question, search_phrase=search_phrase, re=re, answers=answers)

@app.route('/sort_questions/', methods=["POST"])
def sort_questions():
    order_by = request.form['order_by']
    order_direction = request.form['order_direction']
    questions = data_manager.sort_questions(order_by, order_direction)
    return render_template("list.html", headers=QUESTIONS_HEADERS,
                           headers_print=HEADERS_PRINT, questions=questions)

@app.route('/question/<question_id>/new_tag')
def new_tag(question_id):
    tags_name =[]
    tags = data_manager.get_tags(question_id)
    for tag in tags:
        tags_name.append(data_manager.get_tags_name(tag["tag_id"]))
    question = data_manager.get_question(question_id)
    tags_list = data_manager.get_tags_list()
    print ("a")
    return render_template("new_tag.html", headers=QUESTIONS_HEADERS, headers_print=HEADERS_PRINT, question=question,
                           tags_name=tags_name, tags_list=tags_list)


@app.route('/question/<question_id>/add_tag', methods=["GET"])
def add_tag(question_id):
    tag_name = request.args.get('tag')
    for x in tag_name:
        print(x)
    tag_id = data_manager.get_tag_id(tag_name["name"])
    data_manager.add_tag_to_question(question_id, tag_id['name'])
    return redirect(url_for('display_question', question_id=question_id))

if __name__ == '__main__':
    app.run(debug=True)
