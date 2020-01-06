# coding=utf-8
import json
from time import sleep

import requests

headers = {
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'content-length': '0',
    'cookie': 'if_shakespeare=1; __yadk_uid=opj0p7ZJI2kFXV1rf8r2RdHq174HZaBn; locale=zh-CN; read_mode=day; default_font=font2; remember_user_token=W1sxMjM2MTUxOV0sIiQyYSQxMSR0MTNtTzA0bDJySTQ1WGVvZ1VuMUouIiwiMTU3MTcyNjAxOS42OTA3OTA3Il0%3D--47c5a805aa52c0906bc1af4e8c8c7a920a64fbd8; _m7e_session_core=e30d363d0952f0520c6234a20c8b2f15; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216bf5297bfe178-075b921a0092e9-e343166-1049088-16bf5297bff74f%22%2C%22%24device_id%22%3A%2216bf5297bfe178-075b921a0092e9-e343166-1049088-16bf5297bff74f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22desktop%22%2C%22%24latest_utm_medium%22%3A%22not-signed-in-like-note-btn-in-footer%22%7D%2C%22first_id%22%3A%22%22%7D',
    'origin': 'https://www.jianshu.com',
    'referer': 'https://www.jianshu.com/search?q=hexo&page=1&type=note',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'x-csrf-token': 'pBYqpVydSU1nDTcyptju3luD5swz3FzxdJTXQWtfAK0J5XwhiBg0/yXkjGqiXJAL39i6Ttc3T+q+cdCHJD6G2w=='
}

comment = {'content': '按照教程，已将做好了，感觉还行，欢迎大佬指教，\n:yum: :smirk:\n\nhttps://jelly54.github.io/'}

host = 'https://www.jianshu.com/'


# 模拟简书搜索。返回文章详情列表
def search_info(param, page=1):
    search_uri = 'search/do?q=' + param + '&type=note&page=' + str(page) + '&order_by=default'
    rep = requests.post(url=host + search_uri, headers=headers)
    pages_list = json.loads(rep.text)
    if pages_list is None or len(pages_list) < 1:
        print('Exception pages is None.')
    return pages_list['entries']


# 想指定文章发送评论
def send_comments(comments_url, comments_refer):
    headers['referer'] = comments_refer
    rep = requests.post(url=comments_url, headers=headers, data=comment)
    print(rep.status_code)
    print(rep.text)


# 搜索hexo。并将评论写入文章下
def write_comments():
    pages = search_info('hexo', 3)
    for i, page in enumerate(pages):
        node_id = pages[i]['id']
        slug = pages[i]['slug']
        print('Write comments ', i + 1)
        send_comments('https://www.jianshu.com/shakespeare/notes/' + str(node_id) + '/comments',
                      'https://www.jianshu.com/p/' + str(slug))
        sleep(5)


if __name__ == '__main__':
    write_comments()
