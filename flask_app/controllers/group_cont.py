from flask import flash, render_template, request, redirect, session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.expense_mod import Expense
from flask_app.models.group_model import Group
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/group_select')
def select_group():
    groups = Group.get_all_groups()
    return render_template("group_select.html", groups=groups)

@app.route('/create_group')
def create_group():
    return render_template("new_group.html")

@app.route("/add_group", methods=['POST'])
def add_group():
    
    if not Group.validate_group(request.form):
        return redirect("/create_group")
    

    data = {
        "name" : request.form["name"],
        "pin" : request.form["pin"],
    }
    group_id = Group.save(data)
    session['group_id'] = group_id
    print(session['group_id'])
    print(session['user_id'])
    return redirect("/group_select")

@app.route("/add_user_to_group", methods=['POST'])
def user_to_group():
    data = {
        "group_id": request.form['groups']
    }
    group = Group.get_group_by_id(data)
    print(group[0]['pin'])
    print(request.form['pin'])
    
    if request.form['pin'] != group[0]['pin']:
        flash("invalid PIN")
        return redirect("/group_select")
        
    data2 = {
        "group_id" : request.form["groups"],
        "user_id" : session['user_id'],
    }
    Group.save_user_to_group(data2)
    session['group_id'] = request.form['groups']

    return redirect("/expenses/"+session['year']+"/"+session['month'])


