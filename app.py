import bcrypt as bcrypt
import flask
import flask_login
from flask import Flask, request, jsonify,session
from flask_login import LoginManager #new line
import pymongo
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = '*****'  # Change this!
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)

cluster = MongoClient(
    "mongodb+srv://irisgrabois:cwmPS4eqcDpq7QiU@cluster0.phzxmvm.mongodb.net/?retryWrites=true&w=majority")

# create DB cluster reference
db = cluster["BookWorms"]
records = db.users
# insert = {'Email':"irisgrabois@gmmail.com", 'Password': "1234"}
# records.insert_one(insert)

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    # check if login details are correct
    if db.users.count_documents({'Email': email, 'Password': password}, limit=1) != 0:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.jsonify({'status': 'success'})

    return flask.jsonify({'status': 'fail'})



@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in records:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in records:
        return

    user = User()
    user.id = email
    return user
if __name__ == '__main__':
   app.run()