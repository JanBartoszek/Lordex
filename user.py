import server
import data_manager
import database_common

from datetime import datetime
from psycopg2 import sql
from flask import Flask, render_template, redirect, request


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

def add_new_user():
    data_manager.user_dict['id'] = generate_new_id_from_user_table(server.user_table)
    data_manager.user_dict['user_name'] = request.form.get('user_name')
    data_manager.user_dict['user_password'] = request.form.get('user_password')
    data_manager.user_dict['registration_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # dictio = data_manager.question_dict
    # sorted_dict = OrderedDict([(el, data_manager.question_dict[el]) for el in ordination])
    list_to_add = [item for item in data_manager.user_dict.values()]
    data_manager.insert_dict_into_database(server.user_table, list_to_add)