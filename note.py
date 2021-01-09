import datetime

question_dictionary_keys = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
answer_keys = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_question(questions, question_id):
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
    data_string =f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}"
    return data_string


def sorted_list_dictionaries(list_of_dict):
    sorted_list = sorted(list_of_dict, key=lambda k: k['submission_time'])
    return sorted_list
