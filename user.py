import server
import data_manager
import database_common

from datetime import datetime
from psycopg2 import sql
from flask import Flask, render_template, redirect, request


current_user = None

@database_common.connection_handler
def generate_new_id_from_user_table(cursor,table):
    try:
        cursor.execute(
            sql.SQL("""
                        SELECT coalesce(user_id,-1) as user_id FROM {}
                        order by user_id DESC
                        limit 1;
                    """).format(sql.Identifier(table))
                    )
        id_of_the_last_question = cursor.fetchall()
        return id_of_the_last_question[0]['user_id'] + 1
    except IndexError:
        return 1


def check_if_user_exist():
    user_input = request.form.get('user_name')
    user_in_database = data_manager.check_if_user_in_database_return_name(user_input)
    if user_in_database != []:
        user_in_database = user_in_database[0]['user_name']
        if user_input == user_in_database:
            return True
        else:
            return False
    else:
        return False



def add_new_user():
    data_manager.user_dict['id'] = generate_new_id_from_user_table(server.user_table)
    data_manager.user_dict['user_name'] = request.form.get('user_name')
    data_manager.user_dict['user_password'] = request.form.get('user_password')
    data_manager.user_dict['registration_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_manager.user_dict['user_reputation'] = 0
    list_to_add = [item for item in data_manager.user_dict.values()]
    data_manager.insert_dict_into_database(server.user_table, list_to_add)


def change_user_reputation_in_question(item_id, change_by_value):
    user_reputation_and_id = data_manager.check_user_reputation_and_id_in_question(item_id)
    user_reputation_and_id = user_reputation_and_id[0]
    user_reputation = user_reputation_and_id['user_reputation']
    user_reputation = user_reputation + change_by_value
    user_id = user_reputation_and_id['user_id']
    data_manager.change_user_reputation(user_id, user_reputation)


def change_user_reputation_in_answer(item_id, change_by_value):
    user_reputation_and_id = data_manager.check_user_reputation_and_id_in_answer(item_id)
    user_reputation_and_id = user_reputation_and_id[0]
    user_reputation = user_reputation_and_id['user_reputation']
    user_reputation = user_reputation + change_by_value
    user_id = user_reputation_and_id['user_id']
    data_manager.change_user_reputation(user_id, user_reputation)


def change_current_user():
    user_input_login = request.form.get('user_name')
    user_input_password = request.form.get('user_password')
    user_in_database = data_manager.check_if_user_in_database(user_input_login)
    if user_in_database == []:
        check_if_password_correct = "wrong"
        return user_in_database, check_if_password_correct
    check_if_password_correct = data_manager.check_if_password_correct(user_input_login)
    check_if_password_correct = check_if_password_correct[0]['user_password']
    if user_in_database != [] and check_if_password_correct == user_input_password:
        global current_user
        current_user = user_in_database[0]['user_id']
        # change_user_reputation()

        return user_in_database, check_if_password_correct
    else:
        check_if_password_correct = "wrong"
        return user_in_database, check_if_password_correct


def log_out():
    global current_user
    current_user = None


def check_value_of_accepted_button(answer_id):
    value = data_manager.toggle_check_value(answer_id)
    value = value[0]['accepted']
    return value
