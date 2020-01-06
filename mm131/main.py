import time

from mm131.lib.parser import Mm131Parser


def start(path='mm131/', page=None):
    start_time = time.time()
    parser = Mm131Parser(save_path=path)
    parser.get_page(page=page)
    end_time = time.time()
    print('爬取任务已完成,消耗时间:', end_time - start_time)


if __name__ == '__main__':
    start()
    # start(page='list_6_4.html')
