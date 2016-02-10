# coding: utf-8

import datetime
import json
import pdb
import os

from leancloud import Object
from leancloud import Query
from leancloud import LeanCloudError
from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import make_response
from flask import request

from ..util import TiebaPost, updatePage

post_view = Blueprint('post', __name__)

class Tian(Object):
    """日记贴存储日记的class，大致有以下字段
    content: 日记内容
    post_id:
    post_no: 回复楼层
    level_name: 回复者的等级
    user_id: 回复者id
    level_id: 回复者等级
    user_name: 回复者昵称
    user_sex: 回复者性别
    """
    pass


class Test(Object):
    """提供测试的class
    """
    pass


@post_view.route('')
def show():
    """显示前50条日记，直接在leancloud上展示，另有前后端分离页面。
    http://shfshanyue.github.io/diary
    
    Raises:
        e: leancloud不存在class
    
    """
    id = 1
    try:
        # id, 显示id页，每页50条数据
        posts = Query(Tian).ascending('user_id').limit(50).skip(50*(id-1)).find()  
    except LeanCloudError as e:
        if e.code == 101:
            posts = []
        else:
            raise e
    return render_template('tian.html', posts=posts, title=id)

@post_view.route('/api', methods = ['OPTIONS'])
def option():
    res = make_response('OK')
    res.headers['Access-Control-Allow-Method'] = 'POST'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res, 204

@post_view.route('/api', methods = ['GET', 'POST'])
def showApi():
    """给前端提供api接口
        id -> 提供id页的日记，每页50条日记
        user_id -> 提供该user_id的所有日记
    """
    id = int(request.args.get('id', 1))
    user_id = int(request.args.get('user_id', 0))
    try:
        # 如果没有提供user_id，即user_id为0
        if user_id is 0:
            posts = Query(Tian).ascending('post_no').limit(50).skip(50*(id-1)).find()
        else:
            posts = Query(Tian).equal_to('user_id', user_id).limit(500).find()
        code = 200
    except LeanCloudError as e:
        posts = []
        code = '500' + str(e.code)
    data = {
        'code': code,
        'results': [post.dump() for post in posts]
    }
    res = make_response(jsonify(data))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Method'] = 'POST'
    return res

@post_view.route('/add')
def add():
    """全部更新，更新所有页

    """
    updatePage(0)
    return 'success'


@post_view.route('/update', methods=['POST'])
def update():
    """每天更新，更新最后两页

    """
    updatePage(-2)
    return 'success'

