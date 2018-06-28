import user
import data_manager
import logic
import test
from flask import Flask, render_template, redirect, request, session
import requests
from datetime import datetime

question_table = "question"
answer_table = "answer"
comment_table = "comment"
user_table = "user"


app = Flask(__name__)

# comment routings

@app.route('/question/<question_id>/new-comment')
def new_comment_to_question(question_id):
    return render_template('new_comment.html', question_id=question_id, question_table = question_table)
 
@app.route('/question/<question_id>/new-comment',methods=['POST'])
def add_comment_to_question(question_id):
    question_id = int(question_id)
    logic.add_comment(question_id, question_table)
    return redirect('/question/{0}'.format(question_id))

@app.route('/answer/<answer_id>/new-comment')
def new_comment_to_answer(answer_id):
    return render_template('new_comment.html', answer_id=answer_id, answer_table = answer_table)

@app.route('/answer/<answer_id>/new-comment',methods=['POST'])
def add_comment_to_answer(answer_id):
    answer_id = int(answer_id)
    logic.add_comment(answer_id, answer_table)
    question_id = logic.get_question_id_from_answer(answer_id)
    return redirect('/question/{0}'.format(question_id))

@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    logic.delete_comment(comment_id)
    #question_id = logic.get_question_id_from_comment(comment_id)
    return redirect('/')
    #/question/{0}'.format(question_id))

# new question routings

@app.route('/new_question')
def ask_question():
 
    return render_template('new_question.html')


@app.route('/new_question', methods=["POST"])
def add_question():
 
    logic.add_question()
    return redirect('/')


# question routings


@app.route("/question/<question_id>")
def display(question_id):
    question_id = int(question_id)
    view_number = logic.count_views(question_id)
    title = logic.get_data_from_certain_row("title", question_id)
    message = logic.get_data_from_certain_row("message", question_id)
    user_id = logic.get_data_from_certain_row("user_id", question_id)
    user_in_database = user.current_user
    row = logic.display(question_id)
    dict_table = data_manager.get_list_of_dicts_from_database(answer_table)
    tags = data_manager.get_tags_by_question_id(question_id)
    dict_with_comments = data_manager.get_list_of_dicts_from_database(comment_table)
    comment_dict_sorted_by_time = logic.sort_by_time(dict_with_comments)
    return render_template('display_question.html', row=row, question_id=question_id,
                           dict_table=dict_table, message=message, title=title, tags=tags, 
                           comment_dict_sorted_by_time=comment_dict_sorted_by_time, user_in_database=user_in_database, user_id=user_id)


# new answer routings


@app.route("/question/<question_id>/new_answer")
def new_answer(question_id):
    question_id = int(question_id)
    return render_template('new_answer.html', question_id = question_id)


@app.route("/question/<question_id>/new_answer", methods=["POST"])
def add_answer(question_id):
    question_id = int(question_id)
    logic.add_answer(question_id)
    return redirect('/question/{0}'.format(question_id))


# display routings

@app.route('/display_question/post_answer')
def post_answer():
    return render_template('post_answer.html')


# list routings


@app.route('/')
def get_five_questions():
    questions = data_manager.get_five_questions()
    return render_template('list_latest_five_questions.html', dict_sorted_by_time=questions)


@app.route('/list_question')       
def list_question():
    # names=data_manager.get_fieldnames_from_file("sample_data/question.csv")
    dict_from_csv = data_manager.get_list_of_dicts_from_database(question_table)
    dict_sorted_by_time = logic.sort_by_time(dict_from_csv)
    return render_template('list_questions.html', dict_sorted_by_time = dict_sorted_by_time)

@app.route('/', methods=["POST"])
@app.route('/list_question', methods=["POST"])       
def question_vote():
    question_vote = logic.change_vote_value(question_table)
    return redirect('/')


# question routings


@app.route("/question/<question_id>", methods=["POST"])
def answer_vote(question_id):
    question_id = int(question_id)
    question_vote = logic.change_vote_value(answer_table)
    return redirect("/question/{0}".format(question_id))


@app.route('/question/<question_id>/delete')
def delete_question_and_its_answers(question_id):
    question_id = int(question_id)
    data_manager.delete_comments_from_question(question_id)
    data_manager.delete_tags_from_question(question_id)
    logic.delete_question_and_its_answers(question_id)
    return redirect('/')


# answer routings


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    answer_id = int(answer_id)
    question_id = logic.delete_single_answer(answer_table, answer_id)
    return redirect('/question/{}'.format(question_id))


# search routings

@app.route("/search", methods=["POST"])
def search_get_input():
    search_input = logic.get_search_input()
    session['search_input'] = request.form['search_input']
    return redirect('/search')


@app.route("/search")
def search_display():
    if 'search_input' in session:
        search_input = session['search_input']
        questions = data_manager.get_search_questions(search_input)
        answers = data_manager.get_search_answers(search_input)
    return render_template('search.html', questions = questions, answers = answers, search_input = search_input)





# new tag route


@app.route('/question/<question_id>/new_tag', methods=["GET", "POST"])
def new_tag(question_id):
    if request.method == "GET":
        list_of_tags = data_manager.get_tags()
        return render_template('new_tag.html', list_of_tags=list_of_tags, question_id=question_id)
    elif request.method == "POST":
        tag = request.form.get("tag")
        data_manager.insert_tag(question_id, tag)
        return redirect("/question/{}".format(question_id))


@app.route("/new_user")
def add_new_user():
    table = "user"
    id = logic.generate_new_id_from_user_table(table)
    password = "test_password"
    name = "test_name"
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [id, name, password, time]
    data_manager.insert_dict_into_database(table, data)
    return redirect('/')

@app.route("/register")
def register():
    return render_template('register.html')


@app.route("/users_list")
def users_list():
    users_datadict = data_manager.get_list_of_dicts_from_database(user_table)
    return render_template('users_list.html', users_datadict=users_datadict)


@app.route("/register/new_user", methods = ["POST"])
def register_new_user():
    user_in_database = user.check_if_user_exist()
    if user_in_database == False:
        user.add_new_user()
        return redirect('/')
    else:
        return render_template('register.html', user_in_database = user_in_database)



@app.route("/log_in")
def log_in():
    return render_template('log_in.html')

@app.route("/log_in", methods = ["POST"])
def change_current_user():
    user_in_database, check_if_password_correct = user.change_current_user()
    if user_in_database != [] and check_if_password_correct != "wrong":
        return redirect('/')
    else:
        return render_template('log_in.html', user_in_database = user_in_database, check_if_password_correct = check_if_password_correct)

@app.route("/log_out")
def log_out():
    user.log_out()
    return redirect('/')


@app.route("/answer/<answer_id>/toggle_accepted")
def toggle_accepted(answer_id):
    data_manager.toggle_accepted(answer_id)
    value = user.check_value_of_accepted_button(answer_id)
    if value == True:
        user.change_user_reputation_in_answer(answer_id, 15)
    elif value == False:
        user.change_user_reputation_in_answer(answer_id, -15)
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    return redirect('/question/{}'.format(question_id))

@app.route("/user/<user_id>")
def user_profile(user_id):
    user_id = int(user_id)
    question = data_manager.user_questions(user_id)
    answer = data_manager.user_answers(user_id)
    comment = data_manager.user_comments(user_id)
    users_datadict = data_manager.get_list_of_dicts_from_database(user_table)
    count_question = data_manager.count_user_questions(user_id)
    count_answer = data_manager.count_user_answers(user_id)
    count_comment = data_manager.count_user_comments(user_id)
    return render_template("User_profile.html", users_datadict = users_datadict, count_question = count_question, question = question, count_answer = count_answer,answer = answer,count_comment = count_comment, comment = comment, user_id = user_id)

if __name__ == '__main__':
    app.secret_key = 'webex'  
    app.run(
        debug=True,  
        port=5001)
