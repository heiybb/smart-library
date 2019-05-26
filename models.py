"""
Create table modle by sql alchemy
"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


class Book(db.Model):
    """
    Book class
    """
    __tablename__ = "Book"
    BookID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.Text)
    Author = db.Column(db.Text)
    PublishedDate = db.Column(db.Date)
    ISBN = db.Column(db.String(256))

    def __init__(self, Title, Author, PublishedDate, ISBN, BookID = None):
        self.BookID = BookID
        self.Title = Title
        self.Author = Author
        self.PublishedDate = PublishedDate
        self.ISBN = ISBN


class BookSchema(ma.Schema):
    """
    BookSchema
    """
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        # Fields to expose.
        fields = ("BookID", "Title", "Author", "PublishedDate", "ISBN")
