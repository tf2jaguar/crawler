import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

import requests
from lxml import etree


class Mm131Parser:
    def __init__(self, save_path='../mm131/', use_parallel=True):
        self.base_url = 'http://www.mm131.net/xinggan/'
        self.save_path = save_path
        self.use_parallel = use_parallel

    def set_header(self, referer):
        headers = {
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': '{}'.format(self.__set_referer(referer)),
        }
        return headers

    def __set_referer(self, src):
        ref = src[25:-4].split('/')
        if ref[0] == '':
            return self.base_url
        if src[-5:-4] == 1:
            return self.base_url + ref[0] + '.html'
        return self.base_url + ref[0] + '_' + ref[1] + '.html'

    def _ids_titles(self, page=None):
        """
        获取首页中最新的picture id 和 名称
        :param page: 当前第几页
        :return: {id:title} 字典
        """
        url = self.base_url
        if page:
            url += page
        try:
            rep = requests.get(url, headers=self.set_header(''))
            rep.encoding = 'GBK'
            content = etree.HTML(rep.text)
            hrefs = content.xpath('//dl[@class="list-left public-box"]//dd/a/@href')
            titles = content.xpath('//dl[@class="list-left public-box"]//dd/a/img/@alt')

            page_ids_title = {}
            for index, title in enumerate(titles):
                latest_id = hrefs[index][-9:-5]
                page_ids_title[latest_id] = title
            return page_ids_title
        except Exception as e:
            print(e)

    def _ids_titles_for_search(self, key, page='1'):
        key = quote(key.encode('GBK'), 'utf-8')
        url = 'https://www.mm131.net/search/?key=%s&page=%s' % (key, page)
        try:
            rep = requests.get(url=url, headers=self.set_header(''))
            rep.encoding = 'GBK'
            content = etree.HTML(rep.text)
            hrefs = content.xpath('//div[@class="listbox"]//li/a[2]/@href')
            titles = content.xpath('//div[@class="listbox"]//li/a[2]/text()')
            page_count = str(content.xpath('//div[@class="dede_pages"]//a/text()')[-2]).replace('...', '')

            page_ids_title = {}
            for index, title in enumerate(titles):
                latest_id = hrefs[index][-9:-5]
                page_ids_title[latest_id] = title
            return page_ids_title, page_count
        except Exception as e:
            print(e)

    def _one_urls(self, img_id):
        """
        获取一个主题的所有picture下载urls
        :param img_id: picture的id
        :return: 照片下载urls
        """
        url = self.base_url + str(img_id) + ".html"

        rep = requests.get(url, headers=self.set_header(''))
        rep.encoding = 'GBK'
        content = etree.HTML(rep.text)
        count = content.xpath('//span[@class="page-ch"]/text()')[0][1:-1]

        img_urls = []
        for i in range(int(count)):
            _img_url = 'https://img1.mmmw.net/pic/' + str(img_id) + '/' + str(i) + '.jpg'
            img_urls.append(_img_url)
        return img_urls

    def __save(self, pic, folder, name):
        """
        保存一个picture
        :param pic:
        :param folder:
        :param name:
        :return:
        """
        if not self.use_parallel:
            print('save %s' % name, end='---')
        if not os.path.exists(self.save_path + folder):
            os.makedirs(self.save_path + folder)
        with open(self.save_path + '%s/%s' % (folder, name), 'wb') as pp:
            pp.write(pic)
        if not self.use_parallel:
            print('saved!')

    def get_one(self, img_id_title):
        """
        获取一个主题的所有picture
        :param img_id_title: 主题对应的id-主题对应的标题(存储时的文件夹名称)
        :return:
        """
        img_id = img_id_title.split('-')[0]
        title = img_id_title.split('-')[1]
        print('get %s' % title)
        one_urls = self._one_urls(img_id)
        for url in one_urls:
            folder, name = img_id_title, url.split("/")[5]
            resp = requests.get(url, headers=self.set_header(url))
            pic = resp.content
            if resp.status_code == 404:
                print('404 not found!')
            elif resp.status_code == 200:
                self.__save(pic, folder, name)
        print('title %s done.' % title)

    def get_page(self, page=None):
        """
        获取一个页面的所有主题的picture
        :param page: 当前抓取的page页面
        :return:
        """
        print('get %s' % page)
        if self.use_parallel:
            self.get_page_parallel(page=page)
        else:
            ids_titles = self._ids_titles(page)
            for (img_id, img_title) in ids_titles.items():
                self.get_one(str(img_id) + "-" + img_title)
        print('page %s done.' % page)

    def get_all(self):
        # 初始化第一页，自动抓取
        self.get_page()

        # 以下需要根据网站变化做改动，目前总计207页
        for i in range(205):
            page = ''.join(['list_6_', str(i + 2), '.html'])
            self.get_page(page)

    def get_page_parallel(self, works=32, page=None):
        """
        多线程并行下载
        :param works:
        :param page:
        :return:
        """
        ids_titles = self._ids_titles(page)

        with ThreadPoolExecutor(works) as actuator:
            actuator.map(self.get_one, [str(img_id) + "-" + img_title for (img_id, img_title) in ids_titles.items()])

    def search_page(self, key):
        """
        下载指定主题下的所有picture。（单进程）
        :param key: 主题名称
        :return:
        """
        print('search %s' % key)
        ids_titles, page_count = self._ids_titles_for_search(key=key)
        for page in range(2, int(page_count)):
            for (img_id, img_title) in ids_titles.items():
                self.get_one(str(img_id) + "-" + img_title)
            ids_titles, _count = self._ids_titles_for_search(key=key, page=str(page))
        print('search %s done.' % key)

    @staticmethod
    def get_last_task(folder, default=10000):
        """
        TODO 做断点续传。
        思路：获取当前下载的最后一个，重当前这个继续遍历img_id下载。
        :param folder:
        :param default:
        :return:
        """
        if os.path.exists(folder) and len(os.listdir(folder)) > 0:
            return int(min(os.listdir(folder)))
        else:
            return default


if __name__ == '__main__':
    parser = Mm131Parser()
    # 使用并行下载
    parser.use_parallel = True

    # 下载最新页中的主题
    parser.get_page()

    # 下载除最新页之后的其他页面 2~270
    # parser.get_page(page='list_6_2.html')

    # 下载指定主题的picture
    # parser.search_page('周妍希')
    print()
