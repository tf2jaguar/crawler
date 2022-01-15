# -*- coding: utf-8 -*-
"""
@Time    : 2021/2/4 11:33
@Author  : wujungang
@File    : Csdn_click.py
@Function: 模拟用户浏览页面，刷csdn的浏览量
"""
import datetime
from time import sleep
from selenium import webdriver
import requests
import json
import jsonpath
from selenium.webdriver.chrome.options import Options
import random

default_url = {'https://blog.csdn.net/guodong54/article/details/120333178': 0,
               'https://blog.csdn.net/guodong54/article/details/119577856': 0,
               'https://blog.csdn.net/guodong54/article/details/107349914': 0,
               'https://blog.csdn.net/guodong54/article/details/86423315': 0,
               'https://blog.csdn.net/guodong54/article/details/79560097': 0,
               'https://blog.csdn.net/guodong54/article/details/79186547': 0
               }


def print_dict(_dict):
    for key, value in _dict.items():
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('{time} {key}: {value}'.format(time=time_str, key=key, value=value))
    print()


class Csdn_click(object):
    def __init__(self):

        self.total_num = '20'
        self.csdn_url = 'https://blog.csdn.net/community/home-api/v1/get-business-list'
        self.headers = [
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
            {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"},
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"},
            {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)"},
            {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0"},
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201"},
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"}
        ]
        self.data = {
            "page": "1",
            "size": "20",
            "businessType": "blog",
            "noMore": "false",
            "username": "guodong54"
        }

    def exit(self):
        self.driver.quit()

    def get_urls(self):
        """
        获取用户的文章链接列表
        :param locator: xpath定位器
        :data
        :return:
        """

        self.opt = Options()
        self.opt.add_argument("--headless")  # 开启无界面模式
        self.opt.add_argument("--disable-gpu")  # 可选项：禁用gpu，可以解决一些莫名的问题
        self.opt.add_argument("--no-sandbox")
        self.opt.add_argument("--disable-dev-shm-usage")
        self.opt.add_argument(
            'Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9;')
        self.opt.add_argument('Accept-Encoding=gzip, deflate')
        self.opt.add_argument('Host=apps.webofknowledge.com')
        self.opt.add_argument('Upgrade-Insecure-Requests=1')
        self.opt.add_argument(
            'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        self.driver = webdriver.Chrome(options=self.opt)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

        try:
            # 请求数据获取总的文章数
            # res = random.randint(1, 23)
            # response = requests.get(self.csdn_url, params=self.data, headers=self.headers[res])
            # # print(response)
            # json_response = json.loads(response.text)
            # self.total_num = jsonpath.jsonpath(json_response, "$..total")[0]
            # # print(self.total_num)
            #
            # # 获取文章的链接地址列表
            # self.data["size"] = self.total_num
            # response = requests.get(self.csdn_url, params=self.data, headers=self.headers[res])
            # json_response = json.loads(response.text)
            # url_list = jsonpath.jsonpath(json_response, "$..url")
            return list(default_url.keys())
        except Exception as e:
            print(e)
            self.exit()
            self.run()

    def brower_html(self, url_list):
        try:
            for i in url_list:
                # print(i)
                self.driver.get(i)
                js = "return action=document.body.scrollHeight"
                new_height = self.driver.execute_script(js)
                sleep(0.5)
                for j in range(0, new_height, 300):
                    self.driver.execute_script('window.scrollTo(0, %s)' % (j))
                default_url[i] = int(default_url[i]) + 1
            print_dict(default_url)
        except Exception as e:
            print(e)
            self.exit()
            self.run()

    def run(self):
        random_view_times = random.randint(600, 1200)
        while random_view_times != 0:
            url_list = self.get_urls()
            self.brower_html(url_list)
            self.exit()
            random_view_times = random_view_times - 1


if __name__ == '__main__':
    c = Csdn_click()
    c.run()
