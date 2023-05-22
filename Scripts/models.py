from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class User(Document):
    fullname = StringField()
    email = StringField()
    received = BooleanField(default=False)
