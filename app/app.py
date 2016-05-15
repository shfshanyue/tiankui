# coding: utf-8

import pkgutil
import markdown

from datetime import datetime

from flask import Flask, jsonify

from .views.todos import todos_view
from .views.topics import tieba_view
from .views.tiantian import post_view


app = Flask(__name__)

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')
app.register_blueprint(tieba_view, url_prefix='/tieba')
app.register_blueprint(post_view, url_prefix='/tian')


@app.errorhandler(404)
def error_404(error):
    return jsonify({}), 404


