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
            ORDER BY submission_time
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
        WHERE question_id = %(question_id)s
        ORDER BY submission_time
    """

    param = {'question_id': question_id}

    cursor.execute(query, param)
    return cursor.fetchall()

@database_common.connection_handler
def get_answer_question_id(cursor: RealDictCursor, answer_id):
    query = """
        SELECT question_id
        From answer
        WHERE id = %(answer_id)s;
    """

    param = {'answer_id': answer_id}

    cursor.execute(query, param)
    result = cursor.fetchone()
    return result['question_id']

@database_common.connection_handler
def get_question_id(cursor: RealDictCursor, question_id):
    query = """
        SELECT id
        From question
        WHERE id = %(question_id)s;
    """

    param = {'question_id': question_id}

    cursor.execute(query, param)
    result = cursor.fetchone()
    print(result)
    return result['id']

@database_common.connection_handler
def get_answer(cursor: RealDictCursor, answer_id):
    query = """
        SELECT *
        From answer
        WHERE id = %(answer_id)s;
    """

    param = {'answer_id': answer_id}

    cursor.execute(query, param)
    result = cursor.fetchone()
    return result

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
def delete_comment_to_answer(cursor: RealDictCursor, answer_id):
    q_id = get_answer_question_id(answer_id)
    command_comment = """
    DELETE from comment where answer_id=%(answer_id)s
    """

    param_comment = {"answer_id": answer_id}
    cursor.execute(command_comment, param_comment)

    command_comment = """
        DELETE from answer where id=%(answer_id)s
        """

    param_comment = {"answer_id": answer_id}
    cursor.execute(command_comment, param_comment)
    return q_id

@database_common.connection_handler
def delete_one_comment(cursor: RealDictCursor, comment_id, answer_id):
    q_id = get_answer_question_id(answer_id)

    command_comment = """
        DELETE from comment where answer_id=%(answer_id)s and id=%(comment_id)s
        """

    param_comment = {
            "comment_id": comment_id,
            "answer_id": answer_id
            }
    cursor.execute(command_comment, param_comment)
    return q_id

@database_common.connection_handler
def delete_one_comment_q(cursor: RealDictCursor, comment_q_id, question_id):
    q_id = get_question_id(question_id)

    command_comment = """
        DELETE from comment where question_id=%(question_id)s and id=%(comment_q_id)s
        """

    param_comment = {
            "comment_q_id": comment_q_id,
            "question_id": question_id
            }
    cursor.execute(command_comment, param_comment)
    return q_id

@database_common.connection_handler
def get_comments_q(cursor: RealDictCursor):
    command_comment = """
          SELECT * from comment_q
          """
    cursor.execute(command_comment)
    return cursor.fetchall()

@database_common.connection_handler
def get_question_by_anwserid(cursor: RealDictCursor, answer_id):
    command_comment = """
      SELECT id from question where answer_id=%(answer_id)s
      """

    param_comment = {"answer_id": answer_id}
    cursor.execute(command_comment, param_comment)
    q_id = cursor.fetchone()
    return q_id['id']

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

    new_vote_number = vote_n['vote_number']

    command = """
    UPDATE answer 
    SET vote_number = (%(vote_n)s)-1
    WHERE id=%(answer_id)s 
    """
    param ={
        "vote_n": str(new_vote_number),
        'answer_id': str(answer_id)
    }
    cursor.execute(command, param)

    return vote_n['question_id']

@database_common.connection_handler
def save_comment_answer(cursor: RealDictCursor, answer_id, message):
    query_max_id = """
                    SELECT MAX(id) FROM comment
                    """
    cursor.execute(query_max_id)
    new_id = cursor.fetchone()

    if new_id['max']:
        id_comment = new_id['max']
    else:
        id_comment = 1

    edited_count = 0
    sub_t =  data_time_now()
    question_id = get_answer_question_id(answer_id)

    query = "INSERT INTO comment " \
            "VALUES ({},{},{},'{}','{}',{})".format(id_comment+1, question_id, answer_id, message, sub_t, edited_count)

    cursor.execute(query)
    return question_id

@database_common.connection_handler
def get_comments(cursor: RealDictCursor, question_id):
    query = """
    SELECT * from comment WHERE question_id = %(question_id)s
    """
    params = {
        'question_id': question_id
    }
    cursor.execute(query, params)
    com_dict = cursor.fetchall()

    return com_dict

@database_common.connection_handler
def save_comment_question(cursor: RealDictCursor, question_id, message):
    query_max_id = """
                    SELECT MAX(id) FROM comment_q
                    """
    cursor.execute(query_max_id)
    new_id = cursor.fetchone()

    if new_id['max']:
        id_comment = new_id['max']
    else:
        id_comment = 1

    edited_count = 0
    sub_t = data_time_now()
    question_id = get_question_id(question_id)

    query = "INSERT INTO comment_q " \
            "VALUES ({},{},'{}','{}',{})".format(id_comment+1, question_id, message, sub_t, edited_count)
    print(message)
    cursor.execute(query)
    return question_id

@database_common.connection_handler
def save_edit_answer(cursor: RealDictCursor, answer_id, message):
    command = """
        UPDATE answer 
        SET message = (%(message)s)
        WHERE id=%(answer_id)s 
        """
    param = {
        'message': str(message),
        'answer_id': str(answer_id)
    }
    cursor.execute(command, param)
    q_id = get_answer_question_id(answer_id)
    return q_id

@database_common.connection_handler
def save_edit_question(cursor: RealDictCursor, question_id, message, title):
    command = """
        UPDATE question 
        SET message = (%(message)s), title = (%(title)s)
        WHERE id=%(question_id)s 
        """
    param = {
        'message': str(message),
        'title' : str(title),
        'question_id': str(question_id)
    }
    cursor.execute(command, param)
    return None

@database_common.connection_handler
def search(cursor: RealDictCursor, search_phrase):
    query = """
    SELECT question.id,question.submission_time,view_number, question.vote_number,title, question.message
    FROM question
    INNER JOIN answer
        ON question.id = answer.question_id
    WHERE (title ILIKE %(search_phrase)s) or (question.message ILIKE %(search_phrase)s) or (answer.message ILIKE %(search_phrase)s)
    UNION
    SELECT question.id,question.submission_time,view_number, question.vote_number,title, question.message
    FROM question
    WHERE (title ILIKE %(search_phrase)s) or (message ILIKE %(search_phrase)s);
    """
    param = {'search_phrase': f'%{search_phrase}%'}
    cursor.execute(query, param)
    return cursor.fetchall()

@database_common.connection_handler
def get_all_answers(cursor: RealDictCursor):
    query = """
    SELECT question_id, message
    FROM answer
    """
    cursor.execute(query)
    answers = cursor.fetchall()
    return answers

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

@database_common.connection_handler
def delete_question(cursor:RealDictCursor, question_id):
    command1 = """
            DELETE
            FROM comment 
            WHERE question_id=%(id)s
            """
    command2 = """
            DELETE
            FROM comment_q 
            WHERE question_id=%(id)s    
            """
    command3 = """
            DELETE
            FROM answer
            WHERE question_id=%(id)s
            """
    command4 = """
            DELETE
            FROM question 
            WHERE id=%(id)s    
    """
    param = { "id" : str(question_id) }
    cursor.execute(command1, param)
    cursor.execute(command2, param)
    cursor.execute(command3, param)
    cursor.execute(command4, param)
    return None

@database_common.connection_handler
def get_five_questions(cursor: RealDictCursor) -> dict:
    query = """
            SELECT id, submission_time, view_number, vote_number, title
            FROM question
            ORDER by submission_time DESC
            LIMIT 5
            """
    cursor.execute(query)
    questions = cursor.fetchall()
    return questions

@database_common.connection_handler
def sort_questions(cursor: RealDictCursor, order_by, order_direction) -> dict:
    query = """
        SELECT id, submission_time, view_number, vote_number, title
            FROM question
            ORDER by %(order_by)s DESC
            """
    param = {'order_by': order_by}
    cursor.execute(query, param)
    questions = cursor.fetchall()
    return questions

@database_common.connection_handler
def get_answers_id(cursor: RealDictCursor, question_id):
    query = """
        SELECT id
        From answer
        WHERE question_id = %(question_id)s;
    """
    param = {'question_id': question_id}
    cursor.execute(query, param)
    return cursor.fetchall()


@database_common.connection_handler
def delete_question_tag(cursor:RealDictCursor, question_id):
    command = """
            DELETE
            FROM question_tag
            WHERE question_id =%(id)s
            """
    param = {"id": str(question_id)}
    cursor.execute(command, param)
    return None
