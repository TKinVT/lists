from app import app, login
from mongoengine import *
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


USER = app.config["MONGOATLAS_USERNAME"]
PASSWORD = app.config["MONGOATLAS_PASSWORD"]
URL = app.config["MONGOATLAS_URL"]

connect('tkinvt', host=f"mongodb+srv://{USER}:{PASSWORD}@{URL}?retryWrites=true&w=majority")


class User(UserMixin, Document):
    name = StringField(required=True, max_length=30, unique=True)
    email = EmailField(required=True)
    password_hash = StringField()

    def __repr__(self):
        return f"<User: {self.name}>"

    def set_password(self, password):
        password_hash = generate_password_hash(password)
        self.__setattr__("password_hash", password_hash)
        self.save()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.objects.get(id=id)


class List(Document):
    name = StringField(required=True, max_length=30, unique=True)
    description = StringField()
    timestamp = DateTimeField(default=datetime.utcnow)
    creator = ReferenceField(User, reverse_delete_rule=NULLIFY)
    private = BooleanField(default=False)
    checklist = BooleanField(default=True)

    def __repr__(self):
        return f"<List: {self.name}>"


class Item(Document):
    name = StringField(required=True, max_length=120)
    timestamp = DateTimeField(default=datetime.utcnow)
    list = ReferenceField(List, required=True, reverse_delete_rule=CASCADE)
    creator = ReferenceField(User, reverse_delete_rule=NULLIFY)
    completer = ReferenceField(User, reverse_delete_rule=NULLIFY, default=None)
    assignee = ReferenceField(User, reverse_delete_rule=NULLIFY, default=None)
    deadline = DateTimeField(default=None)
    done = BooleanField(default=False)
    done_timestamp = DateTimeField()
    notes = StringField(default=None)

    def __repr__(self):
        return f"<Item: {self.name}>"

    def complete(self):
        # self.completer = user
        self.done = True
        self.done_timestamp = datetime.utcnow
        self.save()

    def uncomplete(self):
        self.completer = None
        self.done = False
        self.done_timestamp = None
        self.save()


######################################
#
# Utlity Functions for handling models
#
######################################

def update_user(name, **items):
    u = User.objects.get(name=name)
    for item in items:
        u.__setattr__(item, items[item])
    u.save()
    return u


def update_list(id, **items):
    l = List.objects.get(id=id)
    for item in items:
        l.__setattr__(item, items[item])
    l.save()
    return l
