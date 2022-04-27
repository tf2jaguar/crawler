import base64
import hashlib
import hmac
import json
import time
import urllib

import requests


class DD_BOT:
    def __init__(self):
        self.ROB_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=bde78b093510c1aec425b6bf3e39e91a97dc55f399161699768b3817aa3c9c93"
        self.ROB_SECRET = 'SECb477b2f1fe71502d00084b487cf437bd42da0909249aaf8d4e467c87847bb907'

    def send(self, _data):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        rep = requests.post(url=self.ROB_WEBHOOK + self.url_suffix(), data=json.dumps(_data), headers=headers)
        rep_json = json.loads(rep.text)
        # print(rep_json)
        if rep_json['errcode']:
            print(rep_json['errmsg'])

    def text_data(self, _content):
        # 返回钉钉机器人所需的文本格式
        text = {
            "msgtype": "text",
            "text": {
                "content": _content
            },
        }
        return text

    def markdown_data(self, _content):
        return {
            "feedCard": {
                "links": [
                    {
                        "title": "时代的火车向前开",
                        "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                        "picURL": "https://gw.alicdn.com/tfs/TB1ayl9mpYqK1RjSZLeXXbXppXa-170-62.png"
                    },
                    {
                        "title": "时代的火车向前开2",
                        "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                        "picURL": "https://gw.alicdn.com/tfs/TB1ayl9mpYqK1RjSZLeXXbXppXa-170-62.png"
                    }
                ]
            },
            "msgtype": "feedCard"
        }

    def url_suffix(self):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.ROB_SECRET.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.ROB_SECRET)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return '&timestamp={}&sign={}'.format(timestamp, sign)


if __name__ == "__main__":
    # 命令行第一个参数为告警内容
    # text_content = sys.argv[1]
    text_content = '测试'
    db = DD_BOT()
    data = db.text_data(text_content)
    # data = markdown_data("")
    db.send(data)
