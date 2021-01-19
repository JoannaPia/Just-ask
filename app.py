from flask import Flask, render_template, request, url_for, redirect
import os
import data_manager


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
    questions = data_manager.get_all_questions()
    return render_template("index.html", headers=QUESTIONS_HEADERS, headers_print=HEADERS_PRINT, questions=questions)


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
                           answers_headers=ANSWERS_HEADERS, answers=answers, headers_print=HEADERS_PRINT, comments=comments)

@app.route('/<int:question_id>/', methods=['GET'])
def display_question_comment(question_id):
    question = data_manager.get_question(question_id)
    answers = data_manager.get_answers(question_id)
    return render_template("display_question_comment.html", headers=QUESTIONS_HEADERS, question=question,
                           answers_headers=ANSWERS_HEADERS, answers=answers, headers_print=HEADERS_PRINT)


@app.route('/save_answer/<int:q_id>', methods=['POST'])
def save_answer(q_id):
    message = request.form['message']
    data_manager.add_answer(data_manager.data_time_now(), '0', q_id, message, str(0))
    return redirect(url_for('display_question', question_id=q_id))

@app.route('/<int:question_id>/new-answer')
def add_answer(question_id):
    return render_template('add_answer.html', question_id=question_id)


@app.route('/delete_question')
def delete_question(question_id):
    pass


@app.route('/answer/<int:answer_id>/delete')
def delete_answer(answer_id):
    question_id = data_manager.delete_answer(answer_id)
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

@app.route('/<int:question_id>/save-comment', methods=['POST'])
def save_comment_question(question_id):
    pass


@app.route('/answer/<int:answer_id>/edit', methods=['GET'])
def edit_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    print(answer['message'])
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

@app.route('/<int:question_id>/vote-up')
def vote_up_on_question(question_id):
    pass


@app.route('/<int:question_id>/vote-down')
def vote_down_on_question(question_id):
    pass


@app.route('/edit_question')
def edit_question(question_id):
    pass

@app.route("/search/", methods=["GET", "POST"])
def search_phrase():
    if request.method == 'POST':
        search_phrase = request.form['search_phrase']
        search_question = data_manager.search(search_phrase)
    return render_template("search_questions.html", headers=QUESTIONS_HEADERS, headers_print=HEADERS_PRINT, questions=search_question)


if __name__ == '__main__':
    app.run(debug=True)
