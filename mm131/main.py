import time

from lib.parser import Mm131Parser


def start(path='mm131/', page=None, parser_all=False):
    """
    按页面抓取主题。
    :param path: 抓取后的picture存储位置。默认为main.py同级目录下的mm131文件夹。
    :param page: 待抓取的页面。第一页为None即可，第2页到第207页，传入*list_6_2.html* 至 *list_6_207.html*
    :param parser_all: 抓取全部网页信息
    :return:
    """
    start_time = time.time()
    parser = Mm131Parser(save_path=path)
    if parser_all:
        parser.get_all()
    else:
        parser.get_page(page=page)
    end_time = time.time()
    print('爬取任务已完成,消耗时间:', end_time - start_time)


if __name__ == '__main__':
    start()  # 抓取当前第一页的图集
    # start(page='list_6_2.html') # 抓取特定某一页的图集
    # start(parser_all=True) # 抓取网站全部图集
