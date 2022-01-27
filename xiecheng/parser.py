import json
import requests

from xiecheng.dd_rob import DD_BOT

default_headers = {
    'authority': 'flights.ctrip.com',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sign': '3ff385553334a58c0b691547c8d4831c',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'scope': 'd',
    'accept': 'application/json',
    'cache-control': 'no-cache',
    'transactionid': 'e879a964ba7942938b5d37600c3d5268',
    'sec-ch-ua-platform': '"macOS"',
    'origin': 'https://flights.ctrip.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://flights.ctrip.com/online/list/oneway-urc-bjs?depdate=2022-02-04&cabin=y_s_c_f&adult=1&child=0&infant=0&containstax=1',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '_RSG=cvKwtZdySb1nLRrwVdZxf9; _RDG=28761c47ad032c24430a076ec0e3327b56; _RGUID=195cf278-f7e9-4e66-9a7b-8e77fad5b571; MKT_CKID=1609929108891.u2dh5.piqf; _abtest_userid=3096dbe8-c0c9-4047-824a-4fa949dd58c0; nfes_isSupportWebP=1; GUID=09031125312066911213; _bfaStatusPVSend=1; StartCity_Pkg=PkgStartCity=1; MKT_Pagesource=PC; appFloatCnt=6; _jzqco=%7C%7C%7C%7C%7C1.1249055168.1609929108888.1640589146244.1642214432230.1640589146244.1642214432230.0.0.0.30.30; __zpspc=9.8.1642214432.1642214432.1%233%7Cwww.google.com%7C%7C%7C%7C%23; ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; FD_SearchHistorty={"type":"S","data":"S%24%u5317%u4EAC%28BJS%29%24BJS%242022-01-18%24%u4E4C%u9C81%u6728%u9F50%28URC%29%24URC%24%24%24"}; Session=smartlinkcode=U135371&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4899&SID=135371&OUID=&createtime=1643164002&Expires=1643768801601; FlightIntl=Search=[%22URC|%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90(URC)|39|URC|480%22%2C%22BJS|%E5%8C%97%E4%BA%AC(BJS)|1|BJS|480%22%2C%222022-02-05%22]; _RF1=123.127.55.43; _bfa=1.1609929104045.35d8h7.1.1643267977486.1643270378396.19.67.10650055217; _bfs=1.1; _bfaStatus=fail'
}

default_parms = {"flightWayEnum": "OW", "arrivalProvinceId": 1,
                 "extGlobalSwitches": {"useAllRecommendSwitch": 'true', "unfoldPriceListSwitch": 'true'},
                 "arrivalCountryName": "中国", "infantCount": 0, "cabin": "Y_S_C_F", "cabinEnum": "Y_S_C_F",
                 "departCountryName": "中国", "flightSegments": [
        {"departureDate": "2022-02-05", "arrivalProvinceId": 1, "arrivalCountryName": "中国", "arrivalCountryCode": "CN",
         "departureCityName": "乌鲁木齐", "departureCityCode": "URC", "departureCountryName": "中国",
         "departureCountryCode": "CN", "arrivalCityName": "北京", "arrivalCityCode": "BJS", "departureCityTimeZone": 480,
         "arrivalCountryId": 1, "timeZone": 480, "departureCityId": 39, "departureCountryId": 1,
         "arrivalCityTimeZone": 480, "departureProvinceId": 29, "arrivalCityId": 1}], "childCount": 0, "segmentNo": 1,
                 "scope": "d", "adultCount": 1,
                 "extensionAttributes": {"LoggingSampling": 'false', "isFlightIntlNewUser": 'false'},
                 "transactionID": "e879a964ba7942938b5d37600c3d5268", "directFlight": 'false', "departureCityId": 39,
                 "isMultiplePassengerType": 0, "noRecommend": 'false', "flightWay": "S", "arrivalCityId": 1,
                 "departProvinceId": 29}


class XC:
    def __init__(self):
        self.query_plane_url = 'https://flights.ctrip.com/international/search/api/search/batchSearch?v=0.32348908805251164'
        self.request = requests.session()
        self.msg = {}

    def query_plane(self, params=None, headers=None):
        if headers is None:
            headers = default_headers
        if params is None:
            params = default_parms
        req = self.request.post(self.query_plane_url, data=json.dumps(params), headers=headers)
        if req.status_code == 200:
            res_json = json.loads(req.text)
            print("res: ", res_json)
            return res_json
        else:
            print(req.status_code, req.text)
            return None

    def get_useful_msg(self):
        plan_json = self.query_plane()
        all_msg = ""
        if plan_json:
            flightItineraryList = plan_json['data']['flightItineraryList']
            for fi in flightItineraryList:
                flightList = fi['flightSegments'][0]['flightList'][0]
                priceList = fi['priceList']
                if flightList['marketAirlineName'] != '中国国航':
                    continue

                all_msg = all_msg + \
                          flightList['marketAirlineName'] + " " + flightList['flightNo'] + flightList['aircraftName'] \
                          + "\n" + flightList['departureDateTime'] + " = " + flightList['arrivalDateTime'] + "\t\t\t" \
                          + "¥" + str(priceList[0]['adultPrice']) + "\n" + \
                          flightList['departureAirportName'] + "           " + flightList['arrivalAirportName'] + "\n\n"
            print(all_msg)
            return all_msg


if __name__ == '__main__':
    xc = XC()
    res = xc.get_useful_msg()
    print(res)
    db = DD_BOT()
    data = db.text_data(res)
    # data = markdown_data("")
    db.send(data)
