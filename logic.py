import server
import data_manager
import user
from datetime import datetime
from collections import OrderedDict

from flask import Flask, render_template, redirect, request
import time

from collections import OrderedDict
from psycopg2 import sql
import database_common

@database_common.connection_handler
def generate_new_id_from_file(cursor,table):
    cursor.execute(
        sql.SQL("""
                    SELECT coalesce(id,-1) as id FROM {}
                      order by id DESC
                      limit 1;
                """).format(sql.Identifier(table))
                   )

    id_of_the_last_question = cursor.fetchall()
    return id_of_the_last_question[0]['id'] +1


@database_common.connection_handler
def get_question_id_from_answer(cursor,answer_id):
    answer_id=str(answer_id)
    cursor.execute(
        sql.SQL("""
                    select question_id from answer
                where id = %s;
                """), str(answer_id)
                   )
    question_id = cursor.fetchall()
    return question_id[0]['question_id']

@database_common.connection_handler
def delete_comment(cursor, comment_id):
    data_manager.delete_dict_from_database(server.comment_table, comment_id)

@database_common.connection_handler
def get_question_id_from_comment(cursor, comment_id):
    comment_id=str(comment_id)


def add_question():
    data_manager.question_dict['id'] = generate_new_id_from_file(server.question_table)
    data_manager.question_dict['submission_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_manager.question_dict['title'] = request.form.get('question')
    data_manager.question_dict['message'] = request.form.get('message')
    data_manager.question_dict['image'] = request.form.get('image')
    data_manager.question_dict['user_id'] = user.current_user
    # dictio = data_manager.question_dict
    # sorted_dict = OrderedDict([(el, data_manager.question_dict[el]) for el in ordination])
    list_to_add = [item for item in data_manager.question_dict.values()]
    data_manager.insert_dict_into_database(server.question_table, list_to_add)


def display(question_id):
    question_dict = data_manager.get_list_of_dicts_from_database(server.question_table)
    for row in question_dict:
        if row['id'] == question_id:
            return row


def add_comment(id_of_question_or_answer, table_type):
    data_manager.comment_dict["id"] = generate_new_id_from_file(server.comment_table)
    if(table_type== 'question'):
        data_manager.comment_dict["answer_id"] = None
        data_manager.comment_dict["question_id"] = id_of_question_or_answer
    if(table_type == "answer"):    
        data_manager.comment_dict["answer_id"] = id_of_question_or_answer
        data_manager.comment_dict["question_id"] = None
    data_manager.comment_dict["message"] = request.form.get('comment')
    data_manager.comment_dict["submission_time"] = datetime.now()
    data_manager.comment_dict['user_id'] = user.current_user
    list_to_add = [item for item in data_manager.comment_dict.values()]
    data_manager.insert_dict_into_database(server.comment_table, list_to_add)

def add_answer(question_id):
    data_manager.answer_dict['id'] = generate_new_id_from_file(server.answer_table)
    data_manager.answer_dict['submission_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_manager.answer_dict['question_id'] = question_id
    data_manager.answer_dict['message'] = request.form.get('answer')
    data_manager.answer_dict['user_id'] = user.current_user
    list_to_add = [item for item in data_manager.answer_dict.values()]
    data_manager.insert_dict_into_database(server.answer_table, list_to_add)


def sort_by_time(dict_list):
    return sorted(dict_list, key=lambda k: k["submission_time"])


def change_vote_value(file):
    list_of_dicts = data_manager.get_list_of_dicts_from_database(file)
    if request.form.get('UP') != None:
        id_of_item_voted_up = int(request.form.get('UP'))
        for row in list_of_dicts:
            if row['id'] == id_of_item_voted_up:
                row['vote_number'] = (int(row['vote_number']) + 1)
                updated_vote_number = row['vote_number']
                arg_list = [updated_vote_number, id_of_item_voted_up]
                data_manager.update_votes_in_database(file, arg_list)
    if request.form.get('DOWN') != None:
        id_of_item_voted_down = int(request.form.get('DOWN'))
        for row in list_of_dicts:
            if row['id'] == id_of_item_voted_down:
                row['vote_number'] = (int(row['vote_number']) - 1)
                updated_vote_number = row['vote_number']
                arg_list = [updated_vote_number, id_of_item_voted_down]
                data_manager.update_votes_in_database(file, arg_list)


def get_data_from_certain_row(field_name, question_id):
    list_of_dicts = data_manager.get_list_of_dicts_from_database(server.question_table)
    value = [row[field_name] for row in list_of_dicts if question_id == row['id']]
    return value[0]

@database_common.connection_handler
def delete_question_and_its_answers(cursor,question_id):
    
    cursor.execute(
        sql.SQL("""
                    select answer.id 
                    from answer join question on (answer.question_id=question.id)
                    where question.id = %s;
                """), str(question_id)
    )
    list_of_dict_with_answer_id_to_delete = cursor.fetchall()
    for dict_with_answer_id in list_of_dict_with_answer_id_to_delete:
        data_manager.delete_dict_from_database(server.answer_table, dict_with_answer_id['id'])
    data_manager.delete_dict_from_database(server.question_table, question_id)
    


def delete_single_answer(answer_table, answer_id):
    list_of_answers = data_manager.get_list_of_dicts_from_database(answer_table)
    for answer in list_of_answers:
        if answer["id"] == answer_id:
            data_manager.delete_dict_from_database(server.answer_table, answer["id"])
            return answer["question_id"]


def count_views(question_id):
    view_number = get_data_from_certain_row("view_number", question_id)
    if request.method == 'GET':
        view_number = int(view_number) + 1
        arg_list = [view_number, question_id]
        data_manager.update_view_number_database(server.question_table, arg_list)
        return view_number


def get_search_input():
    search_input = request.form.get('search_input')
    return search_input

