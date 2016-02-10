# -*- coding: utf-8 -*-
from leancloud import Object
from leancloud import Query
from leancloud import LeanCloudError
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import jsonify

import datetime
import pdb

from ..util import TiebaTopic, Post

tieba_view = Blueprint('tieba', __name__)


class Topic(Object):
    pass


class Rank(Object):
    pass


@tieba_view.route('')
def show():
    try:
        topics = Query(Topic).descending('reply').limit(200).find()
        rank_posts = Query(Rank).descending('post_count').limit(100).find()
        rankReply = Query(Rank).descending('reply_count').limit(50).find()
    except LeanCloudError, e:
        if e.code == 101:
            topics = []
            rank_posts = []
            rankReply = []
        else:
            raise e
    return render_template('tieba.html', topics=topics, rankPosts=rank_posts, rankReplys=rankReply)


@tieba_view.route('/add', methods=['POST'])
def add():
    Topic().clear()
    Rank().clear()
    TiebaTopic().find()
    return 'hello, world'


@tieba_view.route('/collect', methods=['POST'])
def collect():
    querys = Query(Rank).descending('post_count').limit(1000).find()
    for query in querys:
        user = query.get('user')
        reply_count = 0
        for topic in Query(Topic).equal_to('user', user).find():
            reply_count = reply_count + topic.get('reply')
        query.set('reply_count', reply_count)
        query.save()
    return str(len(querys))
