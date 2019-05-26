"""
Route to execute command
"""
from flask import Flask, Blueprint, request, jsonify, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
site = Blueprint("site", __name__)


class Site:
    """
    Site class
    """
    Title = ''
    Author = ''
    PublishedDate = ''
    ISBN = ''
    data = {}
    headers = {}

    @staticmethod
    def get_book_info(request):
        global Title
        global Author
        global PublishedDate
        global ISBN
        global data
        global headers
        Title = request.form["Title"]
        Author = request.form["Author"]
        PublishedDate = request.form["PublishedDate"]
        ISBN = request.form["ISBN"]
        data = {
            "Title": Title,
            "Author": Author,
            "PublishedDate": PublishedDate,
            "ISBN": ISBN,
        }
        headers = {
            "Content-type": "application/json"
        }

    @staticmethod
    def isLogin():
        # check if login status
        if session.get('username') == 'xiaoyu' and session.get('password') == '111':
            user_info = 'xiaoyu'
        else:
            user_info = None
        return user_info

    @staticmethod
    @site.route("/update", methods=['POST'])
    def update():
        user_info = Site.isLogin()
        if user_info is None:
            return render_template("home.html", user_info=user_info)

        method_put = request.form['put']
        Site.get_book_info(request)
        # check if update method
        if method_put == "PUT":
            if len(Title) > 100 or len(Author) > 50:
                flash('The Title or Author is too long! 1. Modify your input. 2. Contact IT suport.', 'danger')
                return redirect(url_for('site.index'))

            book_id = request.form['Id']
            requests.put("http://127.0.0.1:5000/book/" + book_id, data=json.dumps(data), headers=headers)

            flash('The book with ISBN(' + ISBN + ') has been updated successfuly', 'success')
            return redirect(url_for('site.index'))

    @staticmethod
    @site.route("/delete", methods=['POST'])
    def delete():
        user_info = Site.isLogin()
        if user_info is None:
            return render_template("home.html", user_info=user_info)

        method_delete = request.form['delete']
        ISBN = request.form["ISBN"]
        # check if delete method
        if method_delete == 'DELETE':
            id = request.form['Id']
            requests.delete("http://127.0.0.1:5000/book/" + id)

            flash('The book with ISBN(' + ISBN + ') has been deleted successfuly', 'success')
            return redirect(url_for('site.index'))

    @staticmethod
    @site.route("/index", methods=['POST', 'GET'])
    def index():
        user_info = Site.isLogin()
        if user_info is None:
            return render_template("home.html", user_info=user_info)
        # if login status, get data to show in home page
        if request.method == 'GET':
            response = requests.get("http://127.0.0.1:5000/book")
            data = json.loads(response.text)
            return render_template("home.html", book=data, user_info=user_info)

    @staticmethod
    @site.route("/add", methods=['POST','GET'])
    def add():
        user_info = Site.isLogin()
        if user_info is None:
            flash("You haven't login, please login first, then to add book", 'warning')
            return redirect(url_for('site.login'))
        # check if POST which mean to insert a new book
        if request.method == 'POST':
            Site.get_book_info(request)

            if len(Title) > 100 or len(Author) > 50:
                flash('The Title or Author is too long or empty! 1. Modify your input. 2. Contact IT suport.', 'danger')
                return render_template("add.html")

            response = requests.post("http://127.0.0.1:5000/book", data=json.dumps(data), headers=headers)
            res = json.loads(response.text)
            if len(res) == 1:
                flash('The Book has exist! Check ISBN, each book has its unique ISBN', 'danger')
                return render_template("add.html")
            else:
                flash('The Book has added success!', 'success')
                return render_template("add.html")

        return render_template("add.html", user_info=user_info)

    @staticmethod
    @site.route("/report", methods=['POST','GET'])
    def report():
        user_info = Site.isLogin()
        if user_info is None:
            flash("You haven't login, please login first, then to reivew the Report", 'warning')
            return redirect(url_for('site.login'))
        # get the report
        response = requests.get("http://127.0.0.1:5000/book")
        data = json.loads(response.text)
        return render_template("report.html", people=data, user_info=user_info)

    @staticmethod
    @site.route("/login/", methods=['GET','POST'])
    def login():
        # create a from for html
        form = LoginForm()
        # collect form sumbit info
        if form.validate_on_submit():
            if form.username.data == 'xiaoyu' and form.password.data == '111':
                session['username'] = form.username.data
                session['password'] = form.password.data
                flash('You have been logged in!', 'success')
                response = requests.get("http://127.0.0.1:5000/book")
                data = json.loads(response.text)
                user_info = form.username.data
                return render_template("home.html", book=data, user_info=user_info)
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

        user_info = Site.isLogin()
        return render_template('login.html', title='Login', form=form, user_info=user_info)

    @staticmethod
    @site.route("/about")
    def about():
        # this is group member info
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
        user_info = Site.isLogin()
        return render_template("about.html", group=group, user_info=user_info)

    @staticmethod
    @site.route("/logout")
    def logout():
        # logout to delete session
        session.pop('username',None)
        session.pop('password',None)
        return redirect(url_for('site.login'))

    @staticmethod
    @site.route("/register", methods=['GET','POST'])
    def register():
        user_info = Site.isLogin()
        form = RegistrationForm()
        #check is register
        if form.validate_on_submit():
            flash('Account created success!', 'success')
            return render_template('login.html', title='Login', form=form, user_info=user_info)
        return render_template('register.html', title='Register', form=form, user_info=user_info)

