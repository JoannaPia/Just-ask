from psycopg2.extras import RealDictCursor
import database_common


@database_common.connection_handler
def sort_questions(cursor: RealDictCursor, order_by, order_direction):
    if order_direction == 'desc':
        if order_by == "id":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by id DESC
                    """
        elif order_by == "submission_time":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by submission_time DESC
                    """
        elif order_by == "view_number":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by view_number DESC
                    """
        elif order_by == "message":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by id DESC
                    """
        elif order_by == "vote_number":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by vote_number DESC
                    """
        elif order_by == "title":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by title DESC
                    """
    else:
        if order_by == "id":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by id ASC
                    """
        elif order_by == "submission_time":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by submission_time ASC
                    """
        elif order_by == "view_number":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by view_number ASC
                    """
        elif order_by == "message":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by id ASC
                    """
        elif order_by == "vote_number":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by vote_number ASC
                    """
        elif order_by == "title":
            query = """
                    SELECT id, submission_time, view_number, vote_number, title
                    FROM question
                    ORDER by title ASC
                    """
    cursor.execute(query)
    questions = cursor.fetchall()
    return questions
