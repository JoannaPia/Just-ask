import connection

question_file = 'question.csv'
answer_file = 'answer.csv'
question_dictionary_keys = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
answer_keys = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
# question_dictionary_keys = {"id": "Id", "submission_time": "Submission time", "view_number": "View number", "vote_number": "Vote number", "title": "Title", "message": "Message", "image": "Image"}


def get_question(question_id):
    questions = connection.open_file(question_file)
    for question in questions:
        if question["id"] == question_id:
            return question
    return None


def get_answer(answers, question_id):
    display_answers = []
    for answer in answers:
        if answer["question_id"] == question_id:
            display_answers.append(answer)
    return display_answers


def data_time_now():
    now = datetime.datetime.now()
    data_string = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}"
    return data_string


def delete_answer(answer_id):
    temp_answer = {}
    answers = connection.open_file(answer_file)
    for answer in answers:
        if answer["id"] == answer_id:
            temp_answer = answers.pop(answers.index(answer))
    connection.save_answer(answer_file, answers)
    return temp_answer


def vote_up(answer_id):
    answers = connection.open_file(answer_file)
    for answer in answers:
        if answer['id'] == answer_id:
            temp = int(answer['vote_number'])
            temp+= 1
            answer['vote_number'] = str(temp)
            connection.save_answer(answer_file, answers)
            return answer['question_id']


def vote_down(answer_id):
    answers = connection.open_file(answer_file)
    for answer in answers:
        if answer['id'] == answer_id:
            temp = int(answer['vote_number'])
            temp -= 1
            answer['vote_number'] = str(temp)
            connection.save_answer(answer_file, answers)
            return answer['question_id']


def greatest_id():
    max_id = connection.open_file(question_file)
    try:
        return max([int(index_id['id']) for index_id in max_id])
    except ValueError as e:
        return 0


def greatest_id_answer():
    max_id = connection.open_file(answer_file)
    try:
        return max([int(index_id['id']) for index_id in max_id])
    except ValueError as e:
        return 0


def delete_question(question_id):
    questions = connection.open_file(question_file)
    for question in questions:
        if question["id"] == question_id:
            questions.pop(questions.index(question))
    connection.save_questions(question_file, questions)


def add_question(filename, new_question):
    with open(filename, 'a') as f:
        f.write("\n" + new_question)


def add_answer(filename, new_answer):
    with open(filename, 'a') as f:
        f.write("\n" + new_answer + "\n")


def save_to_file(list_of_dict, filename):
    keys = list_of_dict[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dict)


def save_edited_question(updated_question_id, updated_title, updated_message, filename='question.csv'):
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        new_questions = list(reader)
        for question in new_questions:
            if question["id"] == updated_question_id:
                question["title"] = updated_title
                question["message"] = updated_message
    connection.save_questions(question_file, new_questions)


def sort_questions(order_by, order_direction):
    questions = connection.open_file(question_file)
    for key in question_dictionary_keys:
        if order_by == key and order_direction == "asc":
            return sorted(questions, key=itemgetter(key))
        elif order_by == key and order_direction == "desc":
            return sorted(questions, key=itemgetter(key), reverse=True)


def return_question_image_name(image_names, question_id):
    question_image_name = "0"
    for name in image_names:
        if "question" + question_id in name and "answer" not in name:
            question_image_name = name
    return question_image_name


def return_answer_image_names(image_names, question_id):
    answer_image_names = []
    for name in image_names:
        if "question" + question_id in name and "answer" in name:
            answer_image_names.append(name)
    return answer_image_names

