import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import pdfkit
import requests
from Crypto.Cipher import AES


class LaGouParser:
    def __init__(self, save_path='../lg', course_ids='257,', download_article=True, download_video=True,
                 use_parallel=True):
        self.base_url = 'https://kaiwu.lagou.com/'
        self.course_ids = course_ids
        self.course_uri = 'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessons?courseId={}'
        self.article_uri = 'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessonDetail?lessonId={}'
        self.video_uri = 'https://edu-vod.lagou.com/{}/{}?v=1.0.2'
        self.task_queue = []
        self.save_path = save_path
        self.use_parallel = use_parallel
        self.download_article = download_article
        self.download_video = download_video

    def _get_header(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Cookie': 'user_trace_token=20200728211144-5b9e1140-f237-49b0-ae4d-510ea2383b43; _ga=GA1.2.1292131542.1595941906; LGUID=20200728211145-8403d35f-d934-4c73-93f7-04d1b53050a5; LG_HAS_LOGIN=1; LG_LOGIN_USER_ID=9edf44ad9702b1669bac7819b92d2ce2129c025600fa9dfb38bb17fc9ec441ce; user-finger=651d16fc584f492a1e3fe7a9ac257b27; X_HTTP_TOKEN=be30908ab4bc21735561786061810c38e90d91394f; kw_login_authToken="XBjgxf8wVm/2gOILPjplXorQN9mlvOF/Gf2NTMjS6YF7+QkUFLtijxgZWP71plYHBUNAqWUkxoshKxNQqeNGKVhDy0rDeiTloidZpOtmhKCWJ2oglYmDBy75wUFws6lDGhat7ou7qLWftyjSZlrdhoMTSrCaImbnLjN6M3ETJhN4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; gate_login_token=227c2e71d9711c1eaf4f85e74ce7c554eded9872a5578400fa1b00a5bda18198; JSESSIONID=DA499C01EBD2C5A5154E814B0DF2DDA2',
            'Referer': self.base_url,
            'Origin': self.base_url,
            'Sec-fetch-dest': 'empty',
            'Sec-fetch-mode': 'cors',
            'Sec-fetch-site': 'same-site',
            'x-l-req-header': '{deviceType:1}'}

    def _parse_json(self, course_id):
        html = requests.get(url=self.course_uri.format(course_id), headers=self._get_header()).text
        json_msg = json.loads(html)
        # 模块
        message_list = json_msg['content']['courseSectionList']
        course_name = json_msg['content']['courseName']
        # 课程
        for message in message_list:
            model_path = self.save_path + '/'.join(["", course_name, message['sectionName'], ""])
            for i in message['courseLessons']:
                article_name = i['theme']
                article_url = self.article_uri.format(i['id'])
                if i['audioMediaDTO']:
                    file_url = i['audioMediaDTO']['fileUrl']
                else:
                    file_url = None
                self.task_queue.append(Task(article_name, article_url, file_url, model_path))
        return self.task_queue

    def _save_article(self, _url, _name, _save):
        html = requests.get(url=_url, timeout=10, headers=self._get_header()).text
        article_msg = json.loads(html)
        str_html = str(article_msg['content']['textContent'])
        self.html2pdf(str_html, _name, _save)
        return _name

    @staticmethod
    def html2pdf(_html, _name, _save):
        options = {
            'page-size': 'A4',  # Letter
            'encoding': "UTF-8",
            'no-outline': None,
            'custom-header': [('Accept-Encoding', 'gzip')]
        }
        if "|" or '?' or '？' or '/' or '：' in _name:
            _name = _name.replace("|", "-").replace('/', "-").replace('?', "-").replace('？', "-").replace('：', "-")
        _save = _save + 'pdf'
        if not os.path.exists(_save):
            os.makedirs(_save)
        pdfkit.from_string(_html, _save + "/{}.pdf".format(_name), options=options)

    def _save_video(self, _url, _name, _save):
        if not _url:
            return _name
        player_list = []
        write_path = _save + _name + '/'
        key = self.__parse_m3u8(_url, player_list)
        crypto = AES.new(key, AES.MODE_CBC, key)

        for index, ts in enumerate(player_list):
            if not os.path.exists(write_path):
                os.makedirs(write_path)
            res = requests.get(ts, headers=self._get_header())
            with open(write_path + str(index + 1) + '.ts', 'wb') as file:
                file.write(crypto.decrypt(res.content))  # 将解密后的视频写入文件

        c = os.listdir(write_path)
        with open(write_path + '%s.mp4' % _name, 'wb+') as f:
            for i in range(len(c)):
                x = open(write_path + '/' + str(i + 1) + '.ts', 'rb').read()
                f.write(x)
        return _name

    def __parse_m3u8(self, file_url, _list):
        rs = requests.get(file_url, headers=self._get_header()).text
        list_content = rs.split('\n')
        key = ''
        file_id = ''
        for index, line in enumerate(list_content):
            # 判断视频是否经过AES-128加密
            if "#EXT-X-KEY" in line:
                method = line[line.find("METHOD"):line.find(",")].split('=')[1]  # 获取加密方式
                print("Decode Method：", method)
                key_url = line[line.find("URI"):line.rfind('"')].split('"')[1]
                file_id = key_url[key_url.find("vid=") + 4:key_url.rfind('&appId')]
                res = requests.get(key_url, headers=self._get_header())
                key = res.content  # 获取加密密钥
                print("key：", key)
            # 以下拼接方式可能会根据自己的需求进行改动
            if '#EXTINF' in line:
                # 如果加密，直接提取每一级的.ts文件链接地址
                ts_url = self.video_uri.format(file_id, list_content[index + 1])
                _list.append(ts_url)
        return key

    def _parallel_save_pdf(self, works=16):
        """
        多线程并行下载
        :param works:
        :return:
        """
        executor = ThreadPoolExecutor(max_workers=works)
        all_task = [executor.submit(self._save_article, task.article_url, task.file_name, task.save_path)
                    for (task) in self.task_queue]

        for future in as_completed(all_task):
            data = future.result()
            print("in main: get page {} success".format(data))

    def _parallel_save_video(self, works=16):
        """
        多线程并行下载
        :param works:
        :return:
        """
        executor = ThreadPoolExecutor(max_workers=works)
        all_task = [executor.submit(self._save_video, task.file_url, task.file_name, task.save_path)
                    for (task) in self.task_queue]

        for future in as_completed(all_task):
            data = future.result()
            print("in main: get page {} success".format(data))

    def run(self):
        ids = self.course_ids.split(',')
        for i in ids:
            if i:
                self._parse_json(i)
        if self.task_queue:
            if self.use_parallel:
                if self.download_article:
                    self._parallel_save_pdf()
                if self.download_video:
                    self._parallel_save_video()
                return
            for task in self.task_queue:
                if self.download_article:
                    self._save_article(task.article_url, task.file_name, task.save_path)
                if self.download_video:
                    self._save_video(task.file_url, task.file_name, task.save_path)


class Task:
    def __init__(self, file_name, article_url, file_url, save_path='../lg'):
        self.save_path = save_path
        self.file_name = file_name
        self.article_url = article_url
        self.file_url = file_url


if __name__ == '__main__':
    lg = LaGouParser()
    lg.course_ids = '3,64,59'
    lg.download_article = True
    lg.download_video = False
    lg.use_parallel = True
    lg.run()
