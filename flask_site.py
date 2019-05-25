from flask import Flask, Blueprint, request, jsonify, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from forms import RegistrationForm, LoginForm

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
    if request.method == 'POST':

        method_put = request.form['put']
        method_delete = request.form['delete']

        if method_put == "PUT":
            id = request.form['Id']
            Title = request.form["Title"]
            Author = request.form["Author"]
            PublishedDate = request.form["PublishedDate"]
            data = {
                "Title": Title,
                "Author": Author,
                "PublishedDate": PublishedDate,
            }
            headers = {
                "Content-type": "application/json"
            }
            response = requests.put("http://127.0.0.1:5000/book/"+id, data=json.dumps(data), headers=headers)

        elif method_delete == "DELETE":
            id = request.form['Id']
            response = requests.delete("http://127.0.0.1:5000/book/" + id)

        else:

            Title = request.form["Title"]
            Author = request.form["Author"]
            PublishedDate = request.form["PublishedDate"]
            ISBN = request.form["ISBN"]


            if len(Title)>100 or len(Author)>50:
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

        response = requests.get("http://127.0.0.1:5000/book")
        data = json.loads(response.text)
        return render_template("home.html", book=data)

    if request.method == 'GET':
        response = requests.get("http://127.0.0.1:5000/book")
        data = json.loads(response.text)
        return render_template("home.html", book=data)


@site.route("/add", methods=['POST','GET'])
def add():
    return render_template("add.html")


@site.route("/report", methods=['POST','GET'])
def report():
    response = requests.get("http://127.0.0.1:5000/book")
    data = json.loads(response.text)
    return render_template("report.html", people=data)


@site.route("/login/", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'xiaoyu' and form.password.data == '111':
            flash('You have been logged in!', 'success')
            return render_template("home.html")
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@site.route("/about")
def about():
    return render_template("about.html", group=group)


@site.route("/register")
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)