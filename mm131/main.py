import time

from lib.parser import Mm131Parser


def start(path='mm131/', page=None):
    """
    按页面抓取主题。
    :param path: 抓取后的picture存储位置。默认为main.py同级目录下的mm131文件夹。
    :param page: 待抓取的页面。第一页为None即可，第2页到第207页，传入*list_6_2.html* 至 *list_6_207.html*
    :return:
    """
    start_time = time.time()
    parser = Mm131Parser(save_path=path)
    parser.get_page(page=page)
    end_time = time.time()
    print('爬取任务已完成,消耗时间:', end_time - start_time)


if __name__ == '__main__':
    start()
    # start(page='list_6_2.html')
    # start(page='list_6_5.html')
