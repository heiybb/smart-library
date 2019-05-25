from flask import Flask, Blueprint, request, jsonify, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
site = Blueprint("site", __name__)

group = [
    {
        'name': 'Muggle',
        'content': 'IT student at RMIT',
    },
    {
        'name': 'Xiaoyu',
        'content': 'IT student at RMIT',
    },
    {
        'name': 'Hubert',
        'content': 'IT student at RMIT',
    },
    {
        'name': 'Sean',
        'content': 'IT student at RMIT',
    },
]


# Client webpage.
@site.route("/", methods=['POST','GET','PUT','DELETE'])
def index():
    # Use REST API.
    if session.get('username') == 'xiaoyu' and session.get('password') == '111':
        userinfo = 'xiaoyu'
    else:
        userinfo = None

    if request.method == 'POST':

        method_put = request.form['put']
        method_delete = request.form['delete']

        Title = request.form["Title"]
        Author = request.form["Author"]
        PublishedDate = request.form["PublishedDate"]
        ISBN = request.form["ISBN"]


        # update method
        if method_put == "PUT":
            if len(Title) > 100 or len(Author) > 50:
                response = requests.get("http://127.0.0.1:5000/book")
                data = json.loads(response.text)
                flash('The Title or Author is too long! 1. Modify your input. 2. Contact IT suport.', 'danger')
                return render_template("home.html", book=data)

            id = request.form['Id']
            data = {
                "Title": Title,
                "Author": Author,
                "PublishedDate": PublishedDate,
            }
            headers = {
                "Content-type": "application/json"
            }
            requests.put("http://127.0.0.1:5000/book/"+id, data=json.dumps(data), headers=headers)
            response = requests.get("http://127.0.0.1:5000/book")
            data = json.loads(response.text)
            flash('The book with ISBN(' + ISBN + ') has been updated successfuly', 'success')
            return render_template("home.html", book=data, userinfo=userinfo)


        elif method_delete == "DELETE":
            id = request.form['Id']
            requests.delete("http://127.0.0.1:5000/book/" + id)
            response = requests.get("http://127.0.0.1:5000/book")
            data = json.loads(response.text)
            flash('The book with ISBN(' + ISBN + ') has been deleted successfuly', 'success')
            return render_template("home.html", book=data, userinfo=userinfo)

        else:
            if len(Title) > 100 or len(Author) > 50:
                flash('The Title or Author is too long! 1. Modify your input. 2. Contact IT suport.', 'danger')
                return render_template("add.html")



            data = {
                "Title": Title,
                "Author": Author,
                "PublishedDate": PublishedDate,
                "ISBN": ISBN,
            }
            headers = {
                "Content-type": "application/json"
            }
            response = requests.post("http://127.0.0.1:5000/book", data = json.dumps(data), headers = headers)
            data = json.loads(response.text)
            if len(data) == 1:
                flash('The Book has exist! Check ISBN, each book has its unique ISBN', 'danger')
                return render_template("add.html")
            else:
                flash('The Book has added success!', 'success')
                return render_template("add.html")

        # response = requests.get("http://127.0.0.1:5000/book")
        # data = json.loads(response.text)
        # return render_template("home.html", book=data, userinfo=json.dumps(userinfo))

    if request.method == 'GET':

        if session.get('username') == 'xiaoyu' and session.get('password') == '111':
            userinfo = 'xiaoyu'
        else:
            userinfo = None

        response = requests.get("http://127.0.0.1:5000/book")
        data = json.loads(response.text)
        return render_template("home.html", book=data, userinfo=userinfo)


@site.route("/add", methods=['POST','GET'])
def add():
    userinfo = isLogin()
    if request.method == 'POST':
        print(session.get('username'))
        print(session.get('password'))

    return render_template("add.html", userinfo=userinfo)


@site.route("/report", methods=['POST','GET'])
def report():
    userinfo = isLogin()
    response = requests.get("http://127.0.0.1:5000/book")
    data = json.loads(response.text)
    return render_template("report.html", people=data, userinfo=userinfo)


@site.route("/login/", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'xiaoyu' and form.password.data == '111':
            session['username'] = form.username.data
            session['password'] = form.password.data
            flash('You have been logged in!', 'success')
            response = requests.get("http://127.0.0.1:5000/book")
            data = json.loads(response.text)
            userinfo = form.username.data
            return render_template("home.html", book=data, userinfo=userinfo)
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    userinfo = isLogin()
    return render_template('login.html', title='Login', form=form, userinfo=userinfo)


@site.route("/about")
def about():
    userinfo = isLogin()
    return render_template("about.html", group=group, userinfo=userinfo)


@site.route("/logout")
def logout():
    session.pop('username',None)
    session.pop('password',None)
    return redirect(url_for('site.login'))

@site.route("/register")
def register():
    userinfo = isLogin()
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {form.username.data}!', 'success')
        return render_template('login.html', title='Login', form=form, userinfo=userinfo)
    return render_template('register.html', title='Register', form=form, userinfo=userinfo)


def isLogin():
    if session.get('username') == 'xiaoyu' and session.get('password') == '111':
        userinfo = 'xiaoyu'
    else:
        userinfo = None

    return userinfo