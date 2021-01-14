from flask import Flask, render_template, request, url_for, redirect
import os
import data_manager
import datetime

HEADERS_PRINT = {"id": "Question ID", "submission_time": "Submission time", "view_number": "View number",
                 "vote_number": "Vote number", "title": "Title", "message": "Message", "image": "Image"}
QUESTIONS_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWERS_HEADERS = {"id": "Answer ID", "submission_time" : "Submission time", "vote_number": "Vote number",
                   "question_id": "Question ID", "message": "Message", "image": "Image"}
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
TARGET_FOLDER = 'static/images/'
UPLOAD_FOLDER = os.path.join(APP_ROOT, TARGET_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    # Fetch all questions with first row being headers ["id", "submission_time", "view_number", "vote_number",
    # "title", "message", "image"]
    questions = data_manager.get_all_questions()
    return render_template("index.html", headers=QUESTIONS_HEADERS, headers_print=HEADERS_PRINT, questions=questions)


@app.route('/add-question')
def add_question():
    return render_template('add_question.html')


@app.route('/save', methods=['POST'])
def save_question():
    title = request.form['title']
    message = request.form['message']
    id = data_manager.add_question(datetime.datetime.now(), '0', '0', title, message, str(0))
    return redirect(url_for('display_question', question_id=id))


@app.route('/<int:question_id>/', methods=['GET'])
def display_question(question_id):
    question = data_manager.get_question(question_id)
    answers = data_manager.get_answers(question_id)
    return render_template("display_question.html", headers=QUESTIONS_HEADERS, question=question,
                           answers_headers=ANSWERS_HEADERS, answers=answers, headers_print=HEADERS_PRINT)


@app.route('/vote-up/<int:question_id>/<table>')
def vote_up_on_question(question_id, table):
    if table == "question":
        data_manager.vote_up_question(id=question_id)
    questions = data_manager.get_all_questions()
    return render_template("index.html", headers=QUESTIONS_HEADERS, headers_print=HEADERS_PRINT, questions=questions)

@app.route('/vote-down/<int:question_id>/<table>')
def vote_down_on_question(question_id, table):
    if table == "question":
        data_manager.vote_down_question(id=question_id)
    questions = data_manager.get_all_questions()
    return render_template("index.html", headers=QUESTIONS_HEADERS, headers_print=HEADERS_PRINT, questions=questions)


@app.route('/edit_question')
def edit_question(question_id):
    pass


@app.route('/add_answer')
def add_answer(question_id):
    pass


@app.route('/delete_question')
def delete_question(question_id):
    pass


@app.route('/delete_answer')
def delete_answer(answer_id):
    pass


@app.route('/<int:answer_id>/vote-up')
def vote_up_answers(answer_id):
    pass


@app.route('/<int:answer_id>/vote-down')
def vote_down_answers(answer_id):
    pass


@app.route('/<int:answer_id>/vote-down')
def upload_image_answer(answer_id, question_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
