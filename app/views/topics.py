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
from flask import abort

import datetime
import pdb
import collections
import json

from ..util import TiebaTopic, Post

tieba_view = Blueprint('tieba', __name__)


class Topic(Object):
    pass


class Rank(Object):
    pass


def get_month_id(year, month):
    month = unicode(int(month)) if int(month) == month else unicode(month)
    topic = json.load(open('topic.json'))
    return topic[year].get(month)


@tieba_view.route('/<year>/<month>')
def show(year, month):
    month = float(month)
    start, end = get_month_id(year, month), get_month_id(year, month+0.5)
    if end is None:
        end = 1e10
    if start is None:
        abort(404)
    chinese_num = dict(enumerate(u'一二三四五六七八九', start=1))
    chinese_num.update({10: '十', 11: '十一', 12: '十二'})
    chinese_month = chinese_num.get(int(month))
    if float(month) > int(month):
        chinese_month += u'月份下'
    else:
        chinese_month += u'月份上'
    try:
        topics = Query(Topic).less_than("pid", end).greater_than('pid', start)
        top_topics = topics.descending('reply_num').limit(20).find()
        users = [topic.get('author_name')
                 for topic in topics.limit(800).find()]
        users.extend(topic.get('author_name')
                     for topic in topics.limit(800).skip(800).find())
        counter = collections.Counter(users).most_common(20)
    except LeanCloudError, e:
        if e.code == 101:
            topics = []
        else:
            raise e
    return render_template('tieba.html', topics=top_topics, post_rank=counter, month=chinese_month)
