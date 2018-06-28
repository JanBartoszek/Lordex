import csv
import user
from collections import OrderedDict
from psycopg2 import sql, Binary
import database_common
import user


question_dict = {"id": "0", "submission_time": "0", "view_number": "0",
                 "vote_number": "0", "title": "", "message": "", "image": "", "user_id": 0}
answer_dict = {"id": "0", "submission_time": "0", "vote_number": "0", "question_id": "0", "message": "", "image": "", "user_id": 0}
comment_dict = {"id": "0", "question_id": None, "answer_id": None, "message": "", "submission_time": "0", "edited_number":"0", "user_id": 0}
user_dict = {"id": 0, "user_name": "", "user_password": "", "registration_time": "", "user_reputation": 0}

@database_common.connection_handler
def get_list_of_dicts_from_database(cursor, table):
    cursor.execute(
        sql.SQL("""
                    SELECT * FROM {};
                """).format(sql.Identifier(table))
                   )
    list_of_dicts = cursor.fetchall()
    return list_of_dicts


@database_common.connection_handler
def insert_dict_into_database(cursor, table, list_to_add):
    if table == "question":
        cursor.execute(
            sql.SQL("""
                        INSERT INTO {}
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """).format(sql.Identifier(table)),
                        list_to_add
                    )
    if table == "answer":
        cursor.execute(
            sql.SQL("""
                        INSERT INTO {}
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """).format(sql.Identifier(table)),
                        list_to_add
                   )
    if table == "comment":
        cursor.execute(
            sql.SQL("""
                        INSERT INTO {}
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """).format(sql.Identifier(table)),
                        list_to_add
                   )

    if table == "user":
        cursor.execute(
            sql.SQL("""
                        INSERT INTO {}
                        VALUES (%s, %s, %s, %s, %s);
                    """).format(sql.Identifier(table)),
                        list_to_add
                   )


@database_common.connection_handler
def update_votes_in_database(cursor, table, arg_list):
    cursor.execute(
        sql.SQL("""
                    UPDATE {}
                    SET vote_number = %s
                    WHERE id = %s;
                """).format(sql.Identifier(table)),
                    arg_list
                   )


@database_common.connection_handler
def update_view_number_database(cursor, table, arg_list):
    cursor.execute(
        sql.SQL("""
                    UPDATE {}
                    SET view_number = %s
                    WHERE id = %s;
                """).format(sql.Identifier(table)),
                    arg_list
                   )


@database_common.connection_handler
def delete_dict_from_database(cursor, table, item_id):
    cursor.execute(
        sql.SQL("""
                    DELETE FROM {}
                    WHERE id = %(item_id)s;
                """).format(sql.Identifier(table)),
                    {"item_id": str(item_id)}
                   )


# this one is to get latest five questions


@database_common.connection_handler
def get_search_questions(cursor, string):
    # input_var = {'string' : 0}
    # input_var['string'] = 
    cursor.execute(
        sql.SQL("""
                    SELECT *  FROM question
                    WHERE title LIKE  %(string)s;
                """), {'string' : '%' + string + '%'}
                   )
    list_of_dicts = cursor.fetchall()
    return list_of_dicts


@database_common.connection_handler
def get_search_answers(cursor, string):
    cursor.execute(
        sql.SQL("""
                    SELECT answer.*, question.title  FROM answer JOIN question ON answer.question_id = question.id
                    WHERE answer.message LIKE %(string)s
                """), {'string' : '%' + string + '%'}
                   )
    list_of_dicts = cursor.fetchall()
    return list_of_dicts


                #     SELECT question.title, answer.message  FROM question JOIN answer ON question.id = answer.question_id
                #     WHERE title = %(string)s OR answer.message = %(string)s;
                # """), {'string' : string}
                #    )


@database_common.connection_handler
def get_five_questions(cursor):
    cursor.execute("""
                    SELECT *
                    FROM question
                    ORDER BY question.submission_time DESC
                    LIMIT 5;
                   """)
    list_of_dicts = cursor.fetchall()
    return list_of_dicts


# this one is to get all tags


@database_common.connection_handler
def get_tags(cursor):
    cursor.execute("""
                    SELECT *
                    FROM tag;
                   """)
    list_of_dicts = cursor.fetchall()
    return list_of_dicts


# this one is to insert one tag to tag and question_tag tables 


@database_common.connection_handler
def insert_tag(cursor, question_id, tag_name):
    cursor.execute("""
                    INSERT INTO tag (name)
                    SELECT %(tag_name)s
                    WHERE NOT EXISTS
                    (SELECT name FROM tag WHERE name = %(tag_name)s);
                   
                    INSERT INTO question_tag
                    SELECT %(question_id)s, (SELECT DISTINCT id
                                              FROM tag
                                              WHERE name = %(tag_name)s)
                    WHERE NOT EXISTS
                    (SELECT question_id, tag_id 
                    FROM question_tag
                    WHERE question_id = %(question_id)s AND tag_id = (SELECT DISTINCT id
                                                                      FROM tag
                                                                      WHERE name = %(tag_name)s));
                    
                   """, {'question_id': question_id, 'tag_name': tag_name})



# gets all tags added to question 


@database_common.connection_handler
def get_tags_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT DISTINCT name
                    FROM tag
                    JOIN question_tag ON tag.id = tag_id
                    WHERE question_id = (%s);
                   """, (question_id,))
    
    list_of_dicts = cursor.fetchall()
    return list_of_dicts


@database_common.connection_handler
def delete_tags_from_question(cursor, question_id):
    cursor.execute(
        sql.SQL("""
                    DELETE FROM question_tag
                    WHERE question_id = %(question_id)s;
                """), {"question_id": str(question_id)}
                   )


@database_common.connection_handler
def delete_comments_from_question(cursor, question_id):
    cursor.execute(
        sql.SQL("""
                    DELETE FROM comment
                    WHERE question_id = %(question_id)s;
                """), {"question_id": str(question_id)}
                   )

@database_common.connection_handler
def check_if_user_in_database(cursor, user_input):
    cursor.execute(
        sql.SQL("""
                    SELECT user_id FROM "user"
                    WHERE user_name = %(user_input)s;
                """), {'user_input': user_input}
                   )
    user = cursor.fetchall()
    return user


@database_common.connection_handler
def check_if_user_in_database_return_name(cursor, user_input):
    cursor.execute(
        sql.SQL("""
                    SELECT user_name FROM "user"
                    WHERE user_name = %(user_input)s;
                """), {'user_input': user_input}
                )
    user = cursor.fetchall()
    return user


@database_common.connection_handler
def get_user_name_by_user_id(cursor, user_id):
    cursor.execute(
        sql.SQL("""
                    SELECT user_name FROM "user"
                    WHERE user_id = %(user_id)s;
                """), {'user_id': user_id}
                )
    user = cursor.fetchall()
    print(user)
    if user == []:
        return "unlogged"
    else:
        return user[0]['user_name']
    
@database_common.connection_handler
def user_questions(cursor, user_id):
    cursor.execute(
        sql.SQL("""
                    SELECT * FROM "question"
                    WHERE user_id = %s;
                """), str(user_id)
                   )
    user = cursor.fetchall()
    return user


@database_common.connection_handler
def check_if_password_correct(cursor, user_input):
    cursor.execute(
        sql.SQL("""
                    SELECT user_password FROM "user"
                    WHERE user_name = %(user_input)s;
                """), {'user_input': user_input}
                   )
    password = cursor.fetchall()
    return password


@database_common.connection_handler
def check_user_reputation_and_id_in_question(cursor, question_id):
    cursor.execute(
        sql.SQL("""
                    SELECT user_reputation, "user".user_id FROM "user"
                    JOIN question ON "user".user_id = question.user_id
                    WHERE question.id = %(question_id)s;
                """), {'question_id' : question_id}
                   )
    reputation_and_user_id = cursor.fetchall()
    return reputation_and_user_id


@database_common.connection_handler
def check_user_reputation_and_id_in_answer(cursor, answer_id):
    cursor.execute(
        sql.SQL("""
                    SELECT user_reputation, "user".user_id FROM "user"
                    JOIN answer ON "user".user_id = answer.user_id
                    WHERE answer.id = %(answer_id)s;
                """), {'answer_id' : answer_id}
                   )
    reputation_and_user_id = cursor.fetchall()
    return reputation_and_user_id


@database_common.connection_handler
def change_user_reputation(cursor, user_id, reputation_value):
    cursor.execute(
        sql.SQL("""
                    UPDATE "user"
                    SET user_reputation = %(reputation_value)s
                    WHERE user_id = %(user_id)s;
                """), {'user_id' : user_id, 'reputation_value' : reputation_value}
                   )


@database_common.connection_handler
def toggle_accepted(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET accepted = NOT accepted
                    WHERE id = (%s);
                   """, (answer_id,))


@database_common.connection_handler
def toggle_check_value(cursor, answer_id):
    cursor.execute("""
                    SELECT accepted FROM answer
                    WHERE id = (%s);
                   """, (answer_id,)) 
    toggle_value = cursor.fetchall()
    print(toggle_value)
    return toggle_value


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question.id 
                    FROM question
                    JOIN answer on question.id = question_id
                    WHERE answer.id = (%s);
                   """, (answer_id,))

    list_of_dicts = cursor.fetchall()
    return list_of_dicts[0]["id"]


@database_common.connection_handler
def user_answers(cursor, user_id):
    cursor.execute(
        sql.SQL("""
                    SELECT * FROM "answer"
                    WHERE user_id = %s;
                """), str(user_id)
                   )
    user = cursor.fetchall()
    return user


@database_common.connection_handler
def user_comments(cursor, user_id):
    cursor.execute(
        sql.SQL("""
                    SELECT * FROM "comment"
                    WHERE user_id = %s;
                """), str(user_id)
                   )
    user = cursor.fetchall()
    return user



@database_common.connection_handler
def count_user_questions(cursor, user_id):
    cursor.execute(
        sql.SQL("""
                    SELECT COUNT(user_id) FROM "question"
                    WHERE user_id = %s;
                """), str(user_id)
                   )
    user = cursor.fetchall()
    return user

@database_common.connection_handler
def count_user_answers(cursor, user_id):
    cursor.execute(
        sql.SQL("""
                    SELECT COUNT(user_id) FROM "answer"
                    WHERE user_id = %s;
                """), str(user_id)
                   )
    user = cursor.fetchall()
    return user

@database_common.connection_handler
def count_user_comments(cursor, user_id):
    cursor.execute(
        sql.SQL("""
                    SELECT COUNT(user_id) FROM "comment"
                    WHERE user_id = %s;
                """), str(user_id)
                   )
    user = cursor.fetchall()
    return user



