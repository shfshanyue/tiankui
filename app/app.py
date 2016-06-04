# coding: utf-8

import pkgutil
import markdown

from datetime import datetime

from flask import Flask, jsonify, request

from .views.todos import todos_view
from .views.topics import tieba_view
from .views.tiantian import post_view

from leancloud import User
from leancloud import LeanCloudError

app = Flask(__name__)

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')
app.register_blueprint(tieba_view, url_prefix='/tieba')
app.register_blueprint(post_view, url_prefix='/tian')

AccessControl = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, PUT, DELETE, POST, OPTIONS'
}


@app.route('/reg', methods=['POST'])
def reg():
    username = request.form['username']
    password = request.form['password']
    user = User()
    user.set("username", username)
    user.set("password", password)
    user.sign_up()
    return user.get_session_token(), 200, AccessControl


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User()
    try:
        user.login(username, password)
        result = {
            'token': user.get_session_token(),
            'error': 0
        }
    except LeanCloudError as e:
        result = {
            'error': e.error
        }
    return jsonify(result), 200, AccessControl


@app.errorhandler(404)
def error_404(error):
    return jsonify({}), 404


