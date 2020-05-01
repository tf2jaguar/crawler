import json

import requests


class DaLiPan:
    def __init__(self):
        self.host = 'https://www.dalipan.com'

    def _set_header(self, referer=None):
        headers = {
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': '{}'.format(self.__set_referer(referer)),
        }
        return headers

    def __set_referer(self, src):
        if src:
            return src
        return self.host

    def search(self, kw, page='1', diff_day='365'):
        url = self.host + '/api/search?kw=%s&page=%s&diffDay=%s' % (kw, page, diff_day)
        rep = requests.get(url=url, headers=self._set_header())
        data = json.loads(rep.text)

        for file in data['resources']:
            print('id:' + file['res']['id'])
            print('resName:' + file['res']['filename'])
            print('size:' + str(file['res']['size']))

            if file['res']['filelist']:
                for i, sub in enumerate(file['res']['filelist']):
                    print('sub ' + str(i) + ": " + sub['filename'])
            print()

        return data['resources']

    def get_url_pwd(self, res_id):
        url = self.host + '/api/private?id=%s' % res_id
        rep = requests.get(url=url, headers=self._set_header(self.host + '/detail/' + res_id))
        data = json.loads(rep.text)

        print('url: ' + data['url'])
        print('haspwd:' + data['haspwd'])
        print('pwd:' + data['pwd'])


if __name__ == '__main__':
    dali = DaLiPan()
    # dali.search(kw='尚学堂')

    # 替换res_id
    dali.get_url_pwd(res_id='486fc780f4e25cec13ca838d22c2b121')
