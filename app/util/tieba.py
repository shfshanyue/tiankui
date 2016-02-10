# coding: utf-8
from bs4 import BeautifulSoup
import requests
import urllib
import urllib2
import json
import re
import datetime


class Post(object):

    """与需要登陆相关的类，如发帖，签到，
    """

    def __init__(self, username, password):
        self.base_url = 'http://www.baidu.com'
        self.session = requests.Session()
        try:
            self._get_cookies()
        except IOError as e:
            print e
        if self._check_login():
            print 'from cache...'
        else:
            # 防止cookie过期失效
            self.session.cookies.clear()
            self.session.get(self.base_url)
            self.login(username, password)

    def _get_tbs(self):
        url_tbs = 'http://tieba.baidu.com/dc/common/tbs'
        return self.session.get(url_tbs).json()['tbs']

    def _get_token(self):
        url_token = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'
        res = self.session.get(url_token)
        data = json.loads(res.text.replace('\'', '\"'))
        token = data['data']['token']
        return token

    def _get_cookies(self):
        """从文本中获得cookie
        """
        with open('cookie.json') as f:
            cookies = json.load(f)
            self.session.cookies.update(cookies)

    def _check_login(self):
        """验证是否登陆成功

        Returns:
            Boolean: 是否登陆成功
        """
        res = self.session.get(self.base_url)
        match = re.search(u'个人中心', res.text)
        if match:
            return True
        return False

    def post(self, content, tid, kw='太原科技大学', fid='266662'):
        """百度贴吧回复帖子

        Args:
            content (str): 回复帖子的内容 
            tid (str): 回复帖子的ID，http://tieba.baidu.com/p/2674337275，即2674337275
            kw (str, optional): 吧名，即太原科技大学
            fid (str, optional): 吧ID

        Returns:
            TYPE: 百度贴吧的相应json，err_code可查看是否发送成功
        """
        url_post = 'http://tieba.baidu.com/f/commit/post/add'
        tbs = self._get_tbs()
        data = {
            'ie': 'utf-8',
            'kw': kw,
            'fid': fid,
            'tid': tid,
            'content': content,
            'is_login': 1,
            'rich_text': '1',
            'tbs': tbs,
            '__type__': 'reply'
        }
        headers = {
            'Host': 'tieba.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'DNT': '1'
        }
        res = self.session.post(url_post, data=data, headers=headers)
        return res.json()

    def login(self, username, password):
        """登陆百度贴吧，如果登陆成功，保存cookie到json文本，下次登陆可以直接从文本中cookie登陆，无需账号密码

        Args:
            username (str): 百度账号
            password (str): 百度账号密码
        """
        url_login = 'https://passport.baidu.com/v2/api/?login'
        data = {
            'username': username,
            'password': password,
            'u': 'https://passport.baidu.com/',
            'tpl': 'pp',
            'token': self._get_token(),
            'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
            'isPhone': 'false',
            'charset': 'UTF-8',
            'callback': 'parent.bd__pcbs__ra48vi'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://passport.baidu.com/v2/?login',
        }
        res = self.session.post(
            url_login, data=data, headers=headers)
        if self._check_login():
            with open('cookie.json', 'w') as f:
                json.dump(self.session.cookies.get_dict(), f)
            print 'login...'
        else:
            print 'password or username error!'


class TiebaPost(object):

    """爬取贴吧单个帖子的所有回复贴

    Attributes:
        base (str): 帖子的地址，即http://tieba.baidu.com/p/2674337275
    """

    def __init__(self, base):
        self.base = base

    def find_page(self, n):
        """爬取第n页的帖子

        Args:
            n (Intergerr): 第n页

        """
        url = '%s?pn=%d' % (self.base, n)
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find_all(class_='l_post')
        for post in posts:
            info = json.loads(post['data-field'])
            info = dict(info['author'], **info['content'])
            info['date'] = datetime.datetime.strptime(
                info['date'], '%Y-%m-%d %H:%M')
            content = post.find(class_='j_d_post_content')
            del content['class']
            del content['id']
            # 替换掉百度域图片，百度域的图片无法查看
            info['content'] = re.sub(
                r'<img[^<>]*?class="BDE_Image"[^<>]*?>', '', unicode(content))
            yield info
    findPage = find_page

    @property
    def max_page(self):
        """获得帖子的页数
        """
        soup = BeautifulSoup(requests.get(self.base).text, 'html.parser')
        page = soup.find('input', id='jumpPage4')['max-page']
        return int(page)


class TiebaTopic(object):

    def __init__(self, pid=0, kw='太原科技大学'):
        self.kw = kw
        self.pid = pid
        self.base_url = 'http://www.baidu.com'

    def __getitem__(self, key):
        return self.find_page(key, None)

    def find_page(self, page):
        page = page * 50
        url = 'http://tieba.baidu.com/f?kw={0:s}&ie=utf-8&pn={1}'.format(
            self.kw, page)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        j_threads = soup.find_all(class_='j_thread_list')
        for j_thread in j_threads:
            data = json.loads(j_thread['data-field'])
            if data['id'] < self.pid:
                continue
            data['title'] = j_thread.find('a', class_='j_th_tit').get_text()
            yield data
    findPage = find_page
