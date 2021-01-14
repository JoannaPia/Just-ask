from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common
headers = {"id": "Question ID", "submission_time": "Submission time", "view_number": "View number"
            ,"vote_number": "Vote number", "title": "Title", "message": "Message", "image": "Image"}


@database_common.connection_handler
def get_all_questions(cursor: RealDictCursor) -> dict:
    query = """
            SELECT id, submission_time, view_number, vote_number, title
            FROM question
            ORDER BY submission_time
            """
    cursor.execute(query)
    questions = cursor.fetchall()
    return questions

@database_common.connection_handler
def add_question(cursor: RealDictCursor, sub, view_n, vote_n, title, mess, image):
    # update nazwa_tabeli SET nazwa_atrubytu = wartosc WHERE
    query_max_id = """
                    SELECT MAX(id) FROM question
                    """
    cursor.execute(query_max_id)
    new_id = cursor.fetchone()

    nid = new_id['max']

    query = "INSERT INTO question " \
            "VALUES ({},'{}',{},{},'{}','{}','{}')".format(nid+1, sub, view_n, vote_n, title, mess, image)

    cursor.execute(query)
    #connection.commit()
    # conncetion.rollback()
    # Zeby mozna bylo przekierowac na widok nowo stworzonego pytania
    return nid+1

@database_common.connection_handler
def get_question(cursor: RealDictCursor, question_id : str):
    query = """
        SELECT *
        From question
        WHERE id=%(question_id)s     
    """
    param = {'question_id': question_id}
    cursor.execute(query, param)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers(cursor: RealDictCursor, question_id : str):
    query = """
        SELECT *
        From answer
        WHERE question_id=%(question_id)s
    """
    param = {'question_id': question_id}
    cursor.execute(query, param)
    return cursor.fetchall()

@database_common.connection_handler
def vote_up_question(cursor: RealDictCursor, id):
    query="""
    UPDATE question
    SET vote_number = vote_number + 1
    WHERE id=%(id)s
    """
    param = {'id': id}
    cursor.execute(query, param)
    return None

@database_common.connection_handler
def vote_down_question(cursor: RealDictCursor, id):
    query="""
    UPDATE question
    SET vote_number = vote_number - 1
    WHERE id=%(id)s
    """
    param = {'id': id}
    cursor.execute(query, param)
    return None
