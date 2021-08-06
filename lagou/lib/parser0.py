import json
import os
import re
import threading
import time
from queue import Queue

import requests
from Crypto.Cipher import AES


class LaGou_spider():
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Cookie': 'cookie信息',
            'Referer': 'https://kaiwu.lagou.com/course/courseInfo.htm?courseId=17',
            'Origin': 'https://kaiwu.lagou.com',
            'Sec-fetch-dest': 'empty',
            'Sec-fetch-mode': 'cors',
            'Sec-fetch-site': 'same-site',
            'x-l-req-header': '{deviceType:1}'}
        # self.url='https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessons?courseId=46'
        self.queue = Queue()  # 初始化一个队列
        self.error_queue = Queue()

    def get_id(self):
        ture_url_list = []
        html = requests.get(url=self.url, headers=self.headers).text
        dit_message = json.loads(html)
        message_list = dit_message['content']['courseSectionList']
        for message in message_list:
            id1 = message["courseLessons"]
            for t_id in id1:
                ture_url = "https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessonDetail?lessonId={}".format(
                    t_id["id"])
                ture_url_list.append(ture_url)
        return ture_url_list

    def parse_one(self, ture_url_list):
        """

        :return:获得所有的课程url和课程名 返回一个队列（请求一次）
        """
        for ture_url in ture_url_list:
            # print(ture_url)
            html = requests.get(url=ture_url, headers=self.headers).text
            # print(html)
            dit_message = json.loads(html)
            message_list = dit_message['content']
            # print(message_list["videoMedia"])
            if message_list["videoMedia"] == None:
                continue
            else:
                name = message_list["theme"]
                m3u8 = message_list["videoMedia"]["fileUrl"]
                # print(m3u8)
                m3u8_dict = {m3u8: name}  # key为视频的url，val为视频的name
                if os.path.exists("{}.mp4".format(name)):
                    print("{}已经存在".format(name))
                    pass
                else:
                    # print(m3u8_dict)
                    self.queue.put(m3u8_dict)  # 将每个本地不存在的视频url（m3u8）和name加入到队列中
        # for message in message_list:
        #     # print(message)
        #     for i in message['courseLessons']:
        #         if i['videoMediaDTO'] == None:
        #             pass
        #         else:
        #             key = i['videoMediaDTO']['fileUrl']
        #             val = i['theme']
        #             m3u8_dict = {key: val}  # key为视频的url，val为视频的name
        #             # print(m3u8_dict)
        #
        return self.queue

    #
    def get_key(self, **kwargs):
        # global key
        m3u8_dict = kwargs
        # print(m3u8_dict)
        for k in m3u8_dict:  # 获取某个视频的url
            name = ''
            # print(k)
            true_url = k.split('/')[0:-1]
            t_url = '/'.join(true_url)  # 拼接ts的url前面部分
            html = requests.get(url=k, headers=self.headers).text  # 请求返回包含ts以及key数据
            # print(html)
            message = html.split('\n')  # 获取key以及ts的url
            key_parse = re.compile('URI="(.*?)"')
            key_list = key_parse.findall(html)
            # print("密匙链接"+key_list)
            # print(key_list[0])
            key = requests.get(url=key_list[0],
                               headers=self.headers).content  # 一个m3u8文件中的所有ts对应的key是同一个 发一次请求获得m3u8文件的key
            # print(key)
            name1 = m3u8_dict[k]  # 视频的名字
            # print("视频名："+name1)
            if "|" or '?' or '/' in name1:
                name = name1.replace("|", "-")
                for i in message:
                    if '.ts' in i:
                        ts_url = t_url + '/' + i
                        # print("ts_url"+ts_url)
                        self.write(key, ts_url, name, m3u8_dict)
            else:
                name = name1
                for i in message:
                    # print(i)
                    if '.ts' in i:
                        ts_url = t_url + '/' + i
                        # print(ts_url)
                        self.write(key, ts_url, name, m3u8_dict)

    def write(self, key, ts_url, name01, m3u8_dict):
        dir = 'D:\\video'
        if not os.path.exists(dir):
            os.makedirs(dir)
        cryptor = AES.new(key, AES.MODE_CBC, iv=key)
        with open('{}\\{}.mp4'.format(dir, name01), 'ab')as f:
            try:
                html = requests.get(url=ts_url, headers=self.headers).content
                f.write(cryptor.decrypt(html))
                print('{}，{}写入成功'.format(ts_url, name01))
            except Exception as e:
                print('{}爬取出错'.format(name01))
                while True:
                    if f.close():  # 检查这个出问题的文件是否关闭  闭关则删除然后重新爬取，没关闭则等待10s，直到该文件被删除并重新爬取为止
                        os.remove('{}.mp4'.format(name01))
                        print('{}删除成功'.format(name01))
                        thread = self.thread_method(self.get_key, m3u8_dict)
                        print("开启线程{}，{}重新爬取".format(thread.getName(), name01))
                        thread.start()
                        thread.join()
                        break
                    else:
                        time.sleep(10)

    def thread_method(self, method, value):  # 创建线程方法
        thread = threading.Thread(target=method, kwargs=value)
        return thread

    def main(self):
        global m3u8
        thread_list = []
        ture_url_list = self.get_id()
        m3u8_dict = self.parse_one(ture_url_list)
        while not m3u8_dict.empty():
            for i in range(5):  # 创建线程并启动
                if not m3u8_dict.empty():
                    m3u8 = m3u8_dict.get()
                    # print(type(m3u8))
                    thread = self.thread_method(self.get_key, m3u8)
                    thread.start()
                    print(thread.getName() + '启动成功,{}'.format(m3u8))
                    time.sleep(1)
                    thread_list.append(thread)
                else:
                    break
            for k in thread_list:
                k.join()  # 回收线程


if __name__ == "__main__":
    run = LaGou_spider()
    # run.get_id()
    time1 = time.time()
    run.main()
    time2 = time.time()
    print(time2 - time1)
