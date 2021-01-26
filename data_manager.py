from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor, DictCursor
import datetime
import database_common
import answers_data, questions_data

headers = {"id": "Question ID", "submission_time": "Submission time", "view_number": "View number",
           "vote_number": "Vote number", "title": "Title", "message": "Message", "image": "Image"}


def data_time_now():
    now = datetime.datetime.now()
    data_string = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}"
    return data_string


@database_common.connection_handler
def delete_comment_to_answer(cursor: RealDictCursor, answer_id):
    q_id = answers_data.get_answer_question_id(answer_id)
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
    q_id = answers_data.get_answer_question_id(answer_id)
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
    q_id = questions_data.get_question_id(question_id)
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
    sub_t = data_time_now()
    question_id = answers_data.get_answer_question_id(answer_id)

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
    question_id = questions_data.get_question_id(question_id)

    query = "INSERT INTO comment_q " \
            "VALUES ({},{},'{}','{}',{})".format(id_comment+1, question_id, message, sub_t, edited_count)
    print(message)
    cursor.execute(query)
    return question_id


@database_common.connection_handler
def search(cursor: RealDictCursor, search_phrase):
    query = """
    SELECT question.id,question.submission_time,view_number, question.vote_number,title, question.message
    FROM question
    INNER JOIN answer
        ON question.id = answer.question_id
    WHERE (title ILIKE %(search_phrase)s) or (question.message ILIKE %(search_phrase)s) or 
    (answer.message ILIKE %(search_phrase)s)
    UNION
    SELECT question.id,question.submission_time,view_number, question.vote_number,title, question.message
    FROM question
    WHERE (title ILIKE %(search_phrase)s) or (message ILIKE %(search_phrase)s);
    """
    param = {'search_phrase': f'%{search_phrase}%'}
    cursor.execute(query, param)
    return cursor.fetchall()


@database_common.connection_handler
def delete_question_tag(cursor: RealDictCursor, question_id):
    command = """
            DELETE
            FROM question_tag
            WHERE question_id =%(id)s
            """
    param = {"id": str(question_id)}
    cursor.execute(command, param)
    return None


@database_common.connection_handler
def get_tags(cursor: RealDictCursor, question_id):
    query = """
    SELECT *
    FROM question_tag
    WHERE question_id = %(question_id)s; 
    """
    param = {'question_id': question_id}
    cursor.execute(query, param)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags_name(cursor: RealDictCursor, tag_id):
    query = """
    SELECT name
    FROM tag
    WHERE id = %(tag_id)s
    """
    param = {"tag_id": tag_id}
    cursor.execute(query, param)
    return cursor.fetchone()


@database_common.connection_handler
def get_tags_list(cursor: RealDictCursor):
    query = """ 
    SELECT *
    FROM tag
    """
    cursor.execute(query)
    tags_list = cursor.fetchall()
    return tags_list


@database_common.connection_handler
def get_tag_id(cursor: RealDictCursor, tag_name):
    query = """
    SELECT id
    FROM tag
    WHERE name = %(tag_name)s
    """
    param = {"tag_name": tag_name}
    cursor.execute(query, param)
    return cursor.fetchone()


@database_common.connection_handler
def add_tag_to_question(cursor: RealDictCursor, question_id, tag_id):
    command = """
    INSERT INTO question_tag (question_id, tag_id)
    VALUES (%(question_id)s, %(tag_id)s)
    """
    param = {
        "question_id": question_id,
        "tag_id": tag_id
    }
    cursor.execute(command, param)
