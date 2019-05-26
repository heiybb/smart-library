from flask import Flask, Blueprint, request, jsonify, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
site = Blueprint("site", __name__)


class Site:
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
        if session.get('username') == 'xiaoyu' and session.get('password') == '111':
            userinfo = 'xiaoyu'
        else:
            userinfo = None
        return userinfo

    @staticmethod
    @site.route("/update", methods=['POST'])
    def update():
        userinfo = Site.isLogin()
        if userinfo is None:
            return render_template("home.html", userinfo=userinfo)

        method_put = request.form['put']
        Site.get_book_info(request)

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
        userinfo = Site.isLogin()
        if userinfo is None:
            return render_template("home.html", userinfo=userinfo)

        method_delete = request.form['delete']
        ISBN = request.form["ISBN"]

        if method_delete == 'DELETE':
            id = request.form['Id']
            requests.delete("http://127.0.0.1:5000/book/" + id)

            flash('The book with ISBN(' + ISBN + ') has been deleted successfuly', 'success')
            return redirect(url_for('site.index'))


    # Client webpage.
    @staticmethod
    @site.route("/index", methods=['POST', 'GET'])
    def index():
        userinfo = Site.isLogin()
        if userinfo is None:
            return render_template("home.html", userinfo=userinfo)

        if request.method == 'GET':
            response = requests.get("http://127.0.0.1:5000/book")
            data = json.loads(response.text)
            return render_template("home.html", book=data, userinfo=userinfo)

    @staticmethod
    @site.route("/add", methods=['POST','GET'])
    def add():
        userinfo = Site.isLogin()
        if userinfo is None:
            flash("You haven't login, please login first, then to add book", 'warning')
            return redirect(url_for('site.login'))

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

        return render_template("add.html", userinfo=userinfo)

    @staticmethod
    @site.route("/report", methods=['POST','GET'])
    def report():
        userinfo = Site.isLogin()
        if userinfo is None:
            flash("You haven't login, please login first, then to reivew the Report", 'warning')
            return redirect(url_for('site.login'))
        response = requests.get("http://127.0.0.1:5000/book")
        data = json.loads(response.text)
        return render_template("report.html", people=data, userinfo=userinfo)

    @staticmethod
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

        userinfo = Site.isLogin()
        return render_template('login.html', title='Login', form=form, userinfo=userinfo)

    @staticmethod
    @site.route("/about")
    def about():
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
        userinfo = Site.isLogin()
        return render_template("about.html", group=group, userinfo=userinfo)

    @staticmethod
    @site.route("/logout")
    def logout():
        session.pop('username',None)
        session.pop('password',None)
        return redirect(url_for('site.login'))

    @staticmethod
    @site.route("/register", methods=['GET','POST'])
    def register():
        userinfo = Site.isLogin()
        form = RegistrationForm()
        if form.validate_on_submit():
            flash('Account created success!', 'success')
            return render_template('login.html', title='Login', form=form, userinfo=userinfo)
        return render_template('register.html', title='Register', form=form, userinfo=userinfo)

