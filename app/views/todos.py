# coding: utf-8
import datetime
from leancloud import Object, Query, LeanCloudError

from flask import Blueprint, request, redirect, url_for, render_template, jsonify, abort

from ..model import Todo

import datetime

todos_view = Blueprint('todos', __name__)

AccessControl = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, PUT, DELETE, POST, OPTIONS'
}

@todos_view.route('', methods=['GET', 'POST', 'OPTIONS'])
def todos():
    if request.method == 'GET':
        try:
            todos = Query(Todo).limit(800).descending('start').find()
        except LeanCloudError, e:
            if e.code == 101:  
                todos = []
            else:
                raise e
        return jsonify({'results': [todo.dump() for todo in todos]}), 200, AccessControl
    elif request.method == 'OPTIONS':
        return 'ok', 200, AccessControl
    elif request.method == 'POST':
        print 'request.form', request.form
        start = datetime.datetime.fromtimestamp(float(request.form['start']) / 1000)
        end = datetime.datetime.fromtimestamp(float(request.form['end']) / 1000)
        title = request.form['title']
        print 'start:{0} \nend:{1}'.format(start, end)
        print 'start:{0} \nend:{1}'.format(type(start), type(end))
        todo = Todo(start=start, end=end, title=title)
        todo.save()

        return jsonify(todo.dump()), 201, AccessControl


@todos_view.route('/<id>', methods=['GET', 'DELETE', 'PUT', 'OPTIONS'])
def todo(id):
    if request.method == 'GET':
        try:
            todo = Query(Todo).get(id)
            return jsonify(todo.dump()), 200, AccessControl
        except:
            abort(404)
    elif request.method == 'PUT':
        try:
            todo = Query(Todo).get(id)
            title = request.form.get('title')
            todo.set('title', title)
            todo.save()
            return jsonify(todo.dump()), 200, AccessControl
        except:
            abort(404)
    elif request.method == 'DELETE':
        try:
            todo = Query(Todo).get(id)
            todo.destroy()
            return jsonify({}), 204, AccessControl
        except:
            abort(404)
    elif request.method == 'OPTIONS':
        return 'ok', 200, AccessControl
