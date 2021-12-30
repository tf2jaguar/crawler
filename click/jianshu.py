import json
import random
import time
from multiprocessing import Pool

import requests
from tqdm import trange, tqdm

article_list = [
    {
        'article_id': 'f39544e6b3ae',
        'view_count': random.randint(1000, 4000),
    },
    {
        'article_id': '3b7ffc809eca',
        'view_count': random.randint(1000, 4000),
    },
    {
        'article_id': '7ff691cd028e',
        'view_count': random.randint(1000, 4000),
    },
    {
        'article_id': '8d0d4c35f6ff',
        'view_count': random.randint(1000, 4000),
    },
    {
        'article_id': '4ddc8d67f2c8',
        'view_count': random.randint(1000, 4000),
    },
    {
        'article_id': 'c158cd07bd37',
        'view_count': random.randint(1000, 4000),
    }
]


def page_one(_item):
    url = f'https://www.jianshu.com/shakespeare/notes/{_item["article_id"]}/mark_viewed'
    headers = {
        'Content-Type': 'application/json: charset=UTF-8',  # 一定要有的
        'Referer': f'https://www.jianshu.com/p/{_item["article_id"]}',  # 一定要有的
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    post_data = {
        'fuck': 1  # 好名字，并不会增加指定数值的阅读数
    }

    for _ in trange(_item['view_count'], desc=_item['article_id'], leave=True):
        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(post_data), timeout=1)
            time.sleep(0.3)
        except:
            time.sleep(1)


def get_page_parallel(works=6):
    """
    多线程
    :param works:
    :return:
    """
    with Pool(works) as p:
        res = list(tqdm(p.imap(page_one, article_list), total=len(article_list), desc='多进程刷访问量：'))
    p.close()
    p.join()


if __name__ == '__main__':
    get_page_parallel()
