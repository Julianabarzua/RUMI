from flask import flash, render_template, request, redirect, session
from flask_app import app
from flask_app.models.expense_mod import Expense
from flask_app.models.user_model import User
from flask_app.models.group_model import Group
from flask_bcrypt import Bcrypt
import calendar

bcrypt = Bcrypt(app)

@app.route("/expenses/<year>/<month>")
def logedin(year,month):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "id":session['user_id']
    }
    
    data2 = {
        "group_id":session['group_id'],
        "month":month,
        "year":year
    }
    
    expenses = Expense.get_all_from_group(data2)
    usuarioLogeado = User.logedUser(data)
    grupologeado = Group.get_group_by_user_id(data)
    RUMIS = Expense.get_totals_for_users(data2)

    total = 0
    count = 0

    for rumi in RUMIS:
        if rumi['total_amount'] == None:
            rumi['total_amount'] = 0
        total += rumi['total_amount']
        count += 1

    if count == 0:
        average = 0
    else:
        average = round(total/count,2)

    for rumi in RUMIS:
        rumi['result'] = average - rumi['total_amount']

    month_name = calendar.month_name[int(month)]
    
    if int(month) == 1:
        previous_month = 12
        yearp = int(year) -1
    else:
        previous_month = int(month)-1 
        yearp = int(year)

    if int(month) == 12:
        next_month = 1
        yearn = int(year)+1
    else:
        next_month = int(month)+1
        yearn = int(year)


    return render_template("expenses.html", usuarioLogeado = usuarioLogeado, grupologeado=grupologeado, expenses = expenses, RUMIS = RUMIS, total = total, average=average,month_name=month_name, month=int(month), year=int(year), previous_month=previous_month, next_month = next_month, yearn = yearn, yearp=yearp)


@app.route("/expenses/new")
def new_expense():
    print(session['user_id'])

    return render_template("new_expense.html")

@app.route("/add_expense", methods=['POST'])
def add_expense():

    # if not Tvshow.validate_tvshow(request.form):
    #     return redirect("/tvshows/new")
    data = {
        "amount" : request.form["amount"],
        "description" : request.form["description"],
        "posted_by" : session['user_id'],
        "date" : request.form['date']
    }
    Expense.save(data)
    return redirect("/expenses/"+session['year']+"/"+session['month'])

@app.route("/delete_expense/<expense_id>")
def delete_expense(expense_id):
    Expense.delete(id=expense_id)
    return redirect("/expenses/"+session['year']+"/"+session['month'])


@app.route("/expenses/edit/<expense_id>")
def edit_expense(expense_id):
    expense=Expense.getonebyid(expense_id)
    return render_template("edit.html", expense = expense)

@app.route("/expenses/update/<expense_id>", methods=['POST'])
def update_expense(expense_id):

    # if not Tvshow.validate_tvshow(request.form):
    #     return redirect("/tvshows/edit/"+tvshow_id)


    data = {
        "amount" : request.form["amount"],
        "description" : request.form["description"],
        "posted_by" : session['user_id'],
        "date" : request.form['date']
    }
    Expense.update_expense(data, expense_id)
    return redirect("/expenses/"+session['year']+"/"+session['month'])


@app.route("/add_like/<tvshow_id>")
def add_like(tvshow_id):
    data = {
        "show_liked_id" : tvshow_id,
        "user_likes_id" : session['user_id']
    }
    Tvshow.save_like(data)
    return redirect("/tvshows")


@app.route("/delete_like/<tvshow_id>")
def del_like(tvshow_id):
    data = {
        "show_liked_id" : tvshow_id,
        "user_likes_id" : session['user_id']
    }
    Tvshow.del_like(data)
    return redirect("/tvshows")


