import csv
import note

answer_file = 'answer.csv'
from operator import itemgetter


def delete_answer(answer_id):
    temp_answer = {}
    answers = open_file('answer.csv')
    for answer in answers:
        if answer["id"] == answer_id:
            temp_answer = answers.pop(answers.index(answer))
    save_answer('answer.csv', answers)
    return temp_answer


def vote_up(answer_id):
    answers = open_file(answer_file)
    for answer in answers:
        if answer['id'] == answer_id:
            temp = int(answer['vote_number'])
            temp+= 1
            answer['vote_number'] = str(temp)
            save_answer2('answer.csv', answers)
            return answer['question_id']

def vote_down(answer_id):
    answers = open_file(answer_file)
    for answer in answers:
        if answer['id'] == answer_id:
            temp = int(answer['vote_number'])
            temp -= 1
            answer['vote_number'] = str(temp)
            save_answer2('answer.csv', answers)
            return answer['question_id']

def save_answer2(filename, new_answers):
    with open(filename, 'w') as f:
        f.write(','.join(note.answer_keys))
        for answer in new_answers:
            #del answer[None]
            f.write("\n"+','.join(answer.values()))
        f.close()


def delete_question(question_id):
    questions = open_file('question.csv')
    for question in questions:
        if question["id"] == question_id:
            questions.pop(questions.index(question))
    save_questions('question.csv', questions)



def open_file(filename):
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        list_of_dict = list(reader)

    return list_of_dict


def add_question(filename, new_question):
    with open(filename, 'a') as f:
        f.write("\n"+new_question)
        f.close()


def greatest_id():
    max_id = open_file("question.csv")
    try:
        return max([int(index_id['id']) for index_id in max_id])
    except ValueError as e:
        return 0


def greatest_id_answer():
    max_id = open_file("answer.csv")
    try:
        return max([int(index_id['id']) for index_id in max_id])
    except ValueError as e:
        return 0


def add_answer(filename, new_answer):
    with open(filename, 'a') as f:
        f.write("\n" + new_answer + "\n")
        f.close()


def save_answer(filename, new_answers):
    with open(filename, 'w') as f:
        f.write(','.join(note.answer_keys))
        for answer in new_answers:
            f.write("\n" + ','.join(answer.values()))
        f.close()


def save_to_file(list_of_dict, filename):
    keys = list_of_dict[0].keys()
    with open(filename, 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dict)


def save_questions(filename, new_questions):
    with open(filename, "w") as f:
        f.write(','.join(note.question_dictionary_keys))
        for question in new_questions:
            f.write("\n" + ",".join(question.values()))


def save_edited_question(updated_question_id, updated_title, updated_message, filename='question.csv'):
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        new_questions = list(reader)
        for question in new_questions:
            if question["id"] == updated_question_id:
                question["title"] = updated_title
                question["message"] = updated_message
    save_questions('question.csv', new_questions)


def sort_questions(order_by, order_direction):
    questions = open_file('question.csv')
    if order_by == "id":
        if order_direction == "asc":
            return sorted(questions, key=itemgetter("id"))
        elif order_direction == "desc":
            return sorted(questions, key=itemgetter("id"), reverse=True)

    elif order_by == "submission_time":
        if order_direction == "asc":
            return sorted(questions, key=itemgetter("submission_time"))
        elif order_direction == "desc":
            return sorted(questions, key=itemgetter("submission_time"), reverse=True)

    elif order_by == "view_number":
        if order_direction == "asc":
            return sorted(questions, key=itemgetter("view_number"))
        elif order_direction == "desc":
            return sorted(questions, key=itemgetter("view_number"), reverse=True)

    elif order_by == "vote_number":
        if order_direction == "asc":
            return sorted(questions, key=itemgetter("vote_number"))
        elif order_direction == "desc":
            return sorted(questions, key=itemgetter("vote_number"), reverse=True)

    elif order_by == "title":
        if order_direction == "asc":
            return sorted(questions, key=itemgetter("title"))
        elif order_direction == "desc":
            return sorted(questions, key=itemgetter("title"), reverse=True)

    elif order_by == "message":
        if order_direction == "asc":
            return sorted(questions, key=itemgetter("message"))
        elif order_direction == "desc":
            return sorted(questions, key=itemgetter("message"), reverse=True)


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

