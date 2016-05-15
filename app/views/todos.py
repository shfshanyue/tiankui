# coding: utf-8
from leancloud import Object, Query, LeanCloudError

from flask import Blueprint, request, redirect, url_for, render_template, jsonify, abort

from ..model import Todo

todos_view = Blueprint('todos', __name__)


@todos_view.route('', methods=['GET', 'POST'])
def todos():
    if request.method == 'GET':
        try:
            todos = Query(Todo).limit(800).descending('createdAt').find()
        except LeanCloudError, e:
            if e.code == 101:  
                todos = []
            else:
                raise e
        return jsonify({'results': [todo.dump() for todo in todos]})
    elif request.method == 'POST':
        todo = Todo(**request.form.to_dict())
        todo.save()
        return jsonify(todo.dump()), 201


@todos_view.route('/<id>', methods=['GET', 'DELETE', 'PUT'])
def todo(id):
    if request.method == 'GET':
        try:
            todo = Query(Todo).get(id)
            return jsonify(todo.dump()), 200
        except:
            abort(404)
    elif request.method == 'PUT':
        try:
            todo = Query(Todo).get(id)
            title = request.form.get('title')
            todo.set('title', title)
            todo.save()
            return jsonify(todo.dump())
        except:
            abort(404)
    elif request.method == 'DELETE':
        try:
            todo = Query(Todo).get(id)
            todo.destroy()
            return jsonify({}), 204
        except:
            abort(404)
