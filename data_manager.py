from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor, DictCursor
import datetime
import database_common
headers = {"id": "Question ID", "submission_time": "Submission time", "view_number": "View number",
            "vote_number": "Vote number", "title": "Title", "message": "Message", "image": "Image"}

def data_time_now():
    now = datetime.datetime.now()
    data_string = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}"
    return data_string

@database_common.connection_handler
def get_all_questions(cursor: RealDictCursor) -> dict:
    query = """
            SELECT id, submission_time, view_number, vote_number, title
            FROM question
            """
    cursor.execute(query)
    questions = cursor.fetchall()
    return questions

@database_common.connection_handler
def add_question(cursor: RealDictCursor, sub, view_n, vote_n, title, mess, image):
    query_max_id = """
                    SELECT MAX(id) FROM question
                    """
    cursor.execute(query_max_id)
    new_id = cursor.fetchone()
    nid = new_id['max']

    query = "INSERT INTO question " \
            "VALUES ({},'{}',{},{},'{}','{}','{}')".format(nid+1, sub, view_n, vote_n, title, mess, image)

    cursor.execute(query)
    return nid+1

@database_common.connection_handler
def get_question(cursor: RealDictCursor, question_id: int):
    query = """
        SELECT *
        From question
        WHERE id=%(question_id)s     
    """
    param = {'question_id':  str(question_id) }
    cursor.execute(query, param)
    return cursor.fetchone()


@database_common.connection_handler
def get_answers(cursor: RealDictCursor, question_id):
    query = """
        SELECT *
        From answer
        WHERE question_id = %(question_id)s;
    """

    param = {'question_id': question_id}

    cursor.execute(query, param)
    return cursor.fetchall()


@database_common.connection_handler
def add_answer(cursor: RealDictCursor, sub, vote_n, question_id, mess, image):
    query_max_id = """
                SELECT MAX(id) FROM answer
                """
    cursor.execute(query_max_id)
    new_id = cursor.fetchone()

    if new_id['max']:
        nid = new_id['max']
    else:
        nid = 1

    query = "INSERT INTO answer " \
            "VALUES ({},'{}',{},{},'{}','{}')".format(nid + 1, sub, vote_n, question_id, mess, image)

    cursor.execute(query)
    return nid + 1

@database_common.connection_handler
def delete_answer(cursor:RealDictCursor, answer_id):
    question_id_query = "SELECT question_id FROM answer WHERE id={}".format(answer_id)

    cursor.execute(question_id_query)
    question_id = cursor.fetchone()

    command = """
            DELETE
            FROM answer 
            WHERE id=%(answer_id)s
    """
    param = { "answer_id" : answer_id }
    cursor.execute(command, param)
    print(question_id)
    return question_id

@database_common.connection_handler
def vote_up_answer(cursor: RealDictCursor, answer_id):
    query = "SELECT question_id, vote_number FROM answer WHERE id={} ".format(answer_id)
    cursor.execute(query)
    vote_n = cursor.fetchone()

    new_vote_number = vote_n['vote_number'] + 1

    command = """
    UPDATE answer 
    SET vote_number = (%(vote_n)s)
    WHERE id=%(answer_id)s 
    """
    param ={
        "vote_n": str(new_vote_number),
        'answer_id': str(answer_id)
    }
    cursor.execute(command, param)

    return vote_n['question_id']

@database_common.connection_handler
def vote_down_answer(cursor: RealDictCursor, answer_id):
    query = "SELECT question_id, vote_number FROM answer WHERE id={} ".format(answer_id)
    cursor.execute(query)
    vote_n = cursor.fetchone()

    new_vote_number = vote_n['vote_number'] - 1

    command = """
    UPDATE answer 
    SET vote_number = (%(vote_n)s)
    WHERE id=%(answer_id)s 
    """
    param ={
        "vote_n": str(new_vote_number),
        'answer_id': str(answer_id)
    }
    cursor.execute(command, param)

    return vote_n['question_id']
