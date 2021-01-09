from datetime import datetime

from flask import Flask, render_template, url_for,  request, redirect
import note
import data_manager
import os


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
TARGET_FOLDER = 'static/images/'
UPLOAD_FOLDER = os.path.join(APP_ROOT, TARGET_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg'}


@app.route('/')
@app.route('/list')
def index():
    dictionary_keys = note.question_dictionary_keys
    questions = data_manager.open_file("question.csv")
    image_names = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("index.html", headers=dictionary_keys, questions=questions, image_names=image_names)


@app.route('/', methods=["POST"])
def sort_questions():
    order_by = request.form['order_by']
    order_direction = request.form['order_direction']
    questions = data_manager.sort_questions(order_by, order_direction)
    dictionary_keys = note.question_dictionary_keys
    image_names = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("index.html", headers=dictionary_keys, questions=questions,
                           order_by=order_by, order_direction=order_direction, image_names=image_names)


@app.route('/question/<question_id>')
def display_question(question_id):
    dictionary_keys = note.question_dictionary_keys
    answer_keys = note.answer_keys
    questions = data_manager.open_file("question.csv")
    answers = data_manager.open_file("answer.csv") #ZMIENIC
    display_question = note.get_question(questions, question_id)
    display_answers = note.get_answer(answers, question_id)
    image_names = os.listdir(app.config['UPLOAD_FOLDER'])
    question_image_name = data_manager.return_question_image_name(image_names, question_id)
    answer_image_names = data_manager.return_answer_image_names(image_names, question_id)

    return render_template("display_question.html", headers=dictionary_keys, questions=display_question,
                           answers=answer_keys, display_answers=display_answers, question_image_name=question_image_name,
                           answer_image_names=answer_image_names)


@app.route('/edit/<question_id>', methods=["GET"])
def edit_question(question_id):
    questions = data_manager.open_file("question.csv")
    edited_question = note.get_question(questions, question_id)
    return render_template('edit_question.html', question=edited_question)


@app.route('/edit', methods=["POST"])
def save_edited_question():
    updated_question = dict(request.form)
    updated_question_id = updated_question['id']
    updated_title = updated_question['title']
    updated_message = updated_question['message']
    data_manager.save_edited_question(updated_question_id, updated_title, updated_message)
    return redirect(url_for('display_question', question_id=updated_question_id))


@app.route('/add')
def add_question():
    return render_template('add_question.html')


@app.route('/save', methods = ['POST'])
def save_question():

        title = request.form['title']
        message = request.form['message']
        id = data_manager.greatest_id() + 1 #ZMIENIĆ
        new_question = [str(id),
                        str(note.data_time_now()), '0', '0', title, message, str(0)]
        data_manager.add_question('question.csv', ','.join(new_question))
        return redirect(url_for('display_question', question_id=id))



@app.route('/question/<question_id>/new-answer')
def add_answer(question_id):
    return render_template('add_answer.html', question_id=question_id, answer_keys=note.answer_keys)


@app.route('/save_answer/<q_id>', methods=['POST'])
def save_answer(q_id):
    if request.method == 'POST':
        message = request.form['message']
        id_answer = data_manager.greatest_id_answer() + 1
        #id,submission_time,vote_number,question_id,message,image
        new_answer = [str(id_answer), str(note.data_time_now()), '0', q_id, message, str(0)]

        data_manager.add_answer('answer.csv', ','.join(new_answer))
        return redirect(url_for('display_question', question_id=q_id))
    else:
        return redirect(url_for('add_answer', question_id=q_id))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    answer = data_manager.delete_answer(answer_id)
    return redirect(url_for('display_question', question_id=answer['question_id']))

@app.route('/answer/<answer_id>/vote_up')
def vote_up_answers(answer_id):
    q_id = data_manager.vote_up(answer_id)
    print(q_id)
    return redirect(url_for('display_question', question_id=q_id))


@app.route('/answer/<answer_id>/vote_down')
def vote_down_answers(answer_id):
    q_id = data_manager.vote_down(answer_id)
    return redirect(url_for('display_question', question_id=q_id))


@app.route('/vote_question/<question_id>/vote_up')
def vote_up_on_question(question_id):
    questions = data_manager.open_file("question.csv")
    question = note.get_question(questions, question_id)
    vote_number = int(question["vote_number"]) + 1
    question["vote_number"] = str(vote_number)
    data_manager.save_to_file(questions, "question.csv")
    return redirect(url_for("index"))


@app.route('/vote_question/<question_id>/vote_down')
def vote_down_on_question(question_id):
    questions = data_manager.open_file("question.csv")
    question = note.get_question(questions, question_id)
    vote_number = int(question["vote_number"]) - 1
    question["vote_number"] = str(vote_number)
    data_manager.save_to_file(questions, "question.csv")
    return redirect(url_for("index"))

@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for('index'))


@app.route('/question/<question_id>/upload-image', methods=['POST'])
def upload_image_question(question_id):
    file = request.files['file']
    name = file.filename
    extension = name.split(".")[-1]
    file_name = "question"+question_id+"."+extension
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/<answer_id>/upload-image', methods=['POST'])
def upload_image_answer(question_id, answer_id):
    file = request.files['file']
    name = file.filename
    extension = name.split(".")[-1]
    file_name = "question"+question_id+"answer"+answer_id+"."+extension
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    return redirect(url_for('display_question', question_id=question_id))


if __name__ == '__main__':
    app.run(debug=True)