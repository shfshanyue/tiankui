# coding: utf-8

from leancloud import LeanCloudError
from leancloud import Query
from leancloud import Object

from .tieba import TiebaPost
from .tieba import TiebaTopic


class Tian(Object):
    pass


class Topic(Object):
    pass


class TianRank(Object):
    pass


class TopicRank(Object):
    pass


def updatePage(start_page, uid='2674337275'):
    """爬取 http://tieba.baidu.com/p/2674337275 的日记贴，从start_page开始爬取。

    Args:
        uid: 爬取帖子的uid，默认为日记贴
    RETURN:
        count: 爬取成功的帖子数目
    """
    t = TiebaPost('http://tieba.baidu.com/p/{}'.format(uid))
    info = {
        'count': 0,
        'info': [],
    }
    for post in t.find_from_page(start_page):
        try:
            # 如果回复贴已存入数据库，则跳过
            if Query(Tian).equal_to('post_no', post['post_no']).find():
                continue
        except LeanCloudError as e:
            pass
        Tian(**post).save()
        info['count'] += 1
        info['info'].append(
            (post['user_name'], post['post_no']))
        try:
            query = Query(TianRank).equal_to(
                'user_name', post['user_name']).first()
            query.increment('count', 1)
            query.save()
        except LeanCloudError as e:
            # 还没有建class或者没有查询到
            if e.code == 101:
                rank_info = {
                    'user_name': post['user_name'],
                    'count': 1
                }
                TianRank(**rank_info).save()
            else:
                raise e
    return info['count']


def updateTopic(from_page, to_page):
    t = TiebaTopic()
    count = 0
    err = 0
    for data in t.find_to_page(from_page, to_page):
        try:
            query = Query(Topic).equal_to('pid', data['pid']).first()
            query.destroy()
        except LeanCloudError as e:
            if e.code != 101:
                err += 1
                raise e
        finally:
            Topic(**data).save()
            count += 1
    return count, err
