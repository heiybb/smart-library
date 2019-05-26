"""
This is book api which according to Restful api conception
"""
from flask import Flask, Blueprint, request, jsonify, render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app
from models import db, Book, BookSchema
api = Blueprint("api", __name__)

bookSchema = BookSchema()
booksSchema = BookSchema(many=True)


class Api:
    """
    Create Book Api
    """

    # Endpoint to show all books.
    @staticmethod
    @api.route("/book", methods = ["GET"])
    def getBooks():
        book = Book.query.all()
        result = booksSchema.dump(book)
        return jsonify(result.data)

    @staticmethod
    # Endpoint to get book by id.
    @api.route("/book/<id>", methods = ["GET"])
    def getBook(id):
        book = Book.query.get(id)
        return bookSchema.jsonify(book)

    @staticmethod
    # Endpoint to create new book.
    @api.route("/book", methods = ["POST"])
    def addBook():
        title = request.json["Title"]
        author = request.json["Author"]
        published_date = request.json["PublishedDate"]
        isbn = request.json["ISBN"]
        # check if this book has exist
        if len(Book.query.filter(Book.ISBN == ISBN).all()) >= 1:
            temp = {
                'result':'have exist'
            }
            return jsonify(temp)

        new_book = Book(Title = title, Author=author,PublishedDate=published_date,ISBN=isbn)
        db.session.add(new_book)
        db.session.commit()
        return bookSchema.jsonify(new_book)

    @staticmethod
    # Endpoint to update book.
    @api.route("/book/<id>", methods = ["PUT"])
    def bookUpdate(id):
        book = Book.query.get(id)
        title = request.json["Title"]
        author = request.json["Author"]
        published_date = request.json["PublishedDate"]

        #update book
        book.Title = title
        book.Author = author
        book.PublishedDate = published_date
        db.session.commit()
        return bookSchema.jsonify(book)

    @staticmethod
    # Endpoint to delete book.
    @api.route("/book/<id>", methods = ["DELETE"])
    def bookDelete(id):
        book = Book.query.get(id)
        db.session.delete(book)
        db.session.commit()
        return bookSchema.jsonify(book)
