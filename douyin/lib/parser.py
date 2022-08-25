import json
import time
from urllib import parse

from bs4 import BeautifulSoup

import util
from logger import logger


def query_live_status(user_account=None):
    if user_account is None:
        return
    query_url = 'https://live.douyin.com/{}?my_ts={}'.format(user_account, int(time.time()))
    headers = get_headers_for_live()
    response = util.requests_get(query_url, '查询直播状态', headers=headers, use_proxy=True)
    if util.check_response_is_ok(response):
        html_text = response.text
        soup = BeautifulSoup(html_text, "html.parser")
        scripts = soup.findAll('script')
        result = None
        for script in scripts:
            if script.get('id') == 'RENDER_DATA':
                script_string = script.string
                result = parse.unquote(script_string)
                try:
                    result = json.loads(result)
                except TypeError:
                    logger.error('【查询直播状态】json解析错误，user_account：{}'.format(user_account))
                    return None
                break

        if not result or result.get('28').get('status_code') != '0':
            logger.error('【查询直播状态】请求返回异常, {}, user_account：{} '.format(result.get('28'), user_account))
            return

        try:
            room_info = result.get('app').get('initialState').get('roomStore').get('roomInfo')
            room = room_info.get('room')
        except AttributeError:
            logger.error('【查询直播状态】dict取值错误，user_account：{}'.format(user_account))
            return

        if room is None:
            logger.error('【查询直播状态】请求返回room为空，user_account：{}'.format(user_account))
            return

        if room is not None:
            live_status = room.get('status')
            if live_status == 2:
                name = room['owner']['nickname']
                room_title = room['title']
                room_cover_url = room['cover']['url_list'][0]
                qrcode_url = room_info['qrcode_url']

                logger.info('【查询直播状态】【{name}】开播了，准备推送：{room_title}'.format(name=user_account,
                                                                           room_title=room_title))
                # push.push_for_douyin_live(name, qrcode_url, room_title, room_cover_url)

            else:
                logger.info('【查询直播状态】【{name}】未开播 {liveStatus}'.format(name=user_account,
                                                                      liveStatus=live_status))


def get_headers_for_live():
    return {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }


if __name__ == '__main__':
    query_live_status("dayang1886")
