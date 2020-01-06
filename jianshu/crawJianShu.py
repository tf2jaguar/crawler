# coding:utf-8
import json
import re
import requests
from lxml import etree
import MySQLdb

# 头部信息
headers = {
    'Host': "www.jianshu.com",
    'Accept-Language': "zh-CN,zh;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Content-Type': "application/x-www-form-urlencoded",
    'Connection': "keep-alive",
    'Referer': "https://www.jianshu.com/trending/monthly",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
}
# 当前页面有的文章列表
note_list = ""


def insertinto_MySQL(article_url):
    try:
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db='python', port=3306, charset='utf8')
        with conn:
            cursor = conn.cursor()
        html = requests.get(article_url, headers=headers).content
        selector = etree.HTML(html)
        title = selector.xpath('//h1[@class="title"]/text()')[0]
        author = selector.xpath('//span[@class="name"]/a/text()')[0]
        strtime = selector.xpath('//span[@class="publish-time"]/text()')[0]
        word_num = str(selector.xpath('//span[@class="wordage"]/text()')[0]).split(' ')[1]
        view_num = re.findall('"views_count":(.*?),', html, re.S)[0]
        comment_num = re.findall('"comments_count":(.*?),', html, re.S)[0]
        like_num = re.findall('"likes_count":(.*?),', html, re.S)[0]
        id = re.findall('"id":(.*?),', html, re.S)[0]
        # https: // www.jianshu.com / notes / 32433589 / rewards?count = 20
        # 通过正则获取异步加载数据
        gain_url = 'http://www.jianshu.com/notes/{}/rewards?count= 20'.format(id)
        wb_data = requests.get(gain_url, headers=headers)
        json_data = json.loads(wb_data.text)
        # 获取打赏数据
        rewards_num = json_data['rewards_count']
        print(title.encode('utf-8'))
        exec_sql = 'INSERT INTO jianshu_30day (title, author, up_time, word_num, view_num, comment_num, like_num, rewards_num, article_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        exec_data = (title, author, strtime, word_num, view_num, comment_num, like_num, rewards_num, article_url)
        cursor.execute(exec_sql, exec_data)
        conn.commit()
    except MySQLdb.Error as e:
        print(u"连接失败！", str(e))


def get_article_url(url, page_num):
    load_more_url = url + note_list + "page=" + str(page_num)
    html = requests.get(load_more_url, headers=headers).content
    seen_note_list(html)
    selector = etree.HTML(html)
    infos = selector.xpath("//ul[@class='note-list']/li")
    for info in infos:
        article_url_part = 'http://www.jianshu.com' + str(info.xpath('div/a/@href')[0])
        insertinto_MySQL(article_url_part)


def seen_note_list(html):
    ids = re.findall('data-note-id="(\d{8})"', html, re.S)
    global note_list
    for id in ids:
        note_list = note_list + "seen_snote_ids%5B%5D=" + id + "&"


if __name__ == '__main__':
    url = 'http://www.jianshu.com/trending/monthly?'
    for i in range(1, 6):
        get_article_url(url, i)
