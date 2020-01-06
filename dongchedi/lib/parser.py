# -*- coding: utf-8 -*-
import json
import time

import requests
from skimage import io


class MysqlTool:

    def __init__(self, host='localhost', port=3306, user='root', passwd='123456', db='craw', charset='utf8'):
        import pymysql
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)

    def execute(self, exe_sql):
        exe_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        log = open("mysql_log.txt", "a", encoding='utf-8')
        res = None
        cur = self.conn.cursor()
        try:
            status = cur.execute(exe_sql)
            self.conn.commit()
            res = status, cur.fetchall()
            log.writelines(exe_time + " " + exe_sql + "\n" + str(res) + "\n")
        except Exception as e:
            print(e)
            log.writelines(exe_time + " " + exe_sql + "\n" + str(e) + "\n")
            self.conn.rollback()
        finally:
            cur.close()
            self.conn.close()
        return res


header = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'tt_webid=6760477537370965518',
    'origin': 'https://www.dcdapp.com',
    'referer': 'https://www.dcdapp.com/auto',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.2804.97'
}


def request_car_series(brand_id):
    url = 'https://www.dcdapp.com/motor/brand/m/v1/select/series/?city_name=%E5%8C%97%E4%BA%AC'
    param = {
        'offset': 0,
        'limit': 1000,
        'is_refresh': 1,
        'city_name': '北京',
        'brand': brand_id
    }
    rep = requests.post(url=url, data=param, headers=header)
    rep_json = json.loads(rep.text)
    if rep_json['status'] == 'success':
        return rep_json['data']['series']
    else:
        raise Exception("get car series has exception!")


def request_more_car(category, series_id, offset):
    url = 'https://www.dcdapp.com/motor/car_page/v3/get_picture/?version_code=445&category=' + str(category) + \
          '&series_id=' + str(series_id) + '&offset=' + str(offset) + '&car_id=null'
    # print(url)
    car_request_filed = open("data/car_request_filed.txt", "a", encoding='utf-8')
    time.sleep(0.25)
    rep = requests.get(url=url, headers=header)
    rep_json = json.loads(rep.text)
    if rep_json['status'] == 0:
        if not rep_json.get('data').get('paging'):
            rep_json = request_more_car(category, series_id, offset)
        if not rep_json:
            print("try exception!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            car_request_filed.writelines(",".join([category, str(series_id), str(offset), "\n"]))
            return None
        print("[series]:", series_id, " [craw]:", rep_json['data']['paging']['offset'], "[total]:",
              rep_json['data']['paging']['total_count'])
        return rep_json
    else:
        car_request_filed.writelines(",".join([category, series_id, offset, "\n"]))
        raise Exception("get car series has exception!")


# category:
# car_series: 车所有型号
# offset: 0~n  从0开始每次加30  paging:中有描述是否还有更多
def get_car_image_by_series(category, series):
    for i, car_se in enumerate(series):
        get_car_image_by_concern_id(category, car_se['concern_id'], 0)


# 根据车ID 获取车image信息
# category: 查询分类  wg
# concern_id: 车ID
# ofset: 偏移量
def get_car_image_by_concern_id(category, concern_id, ofset):
    rep_json = request_more_car(category, concern_id, ofset)
    get_car_image_by_json(category, concern_id, rep_json, ofset)


#  从懂车帝 抓取的json中提取 每种车型的image
# category: 查询分类  wg
# concern_id: 车ID
# rep_json: @request_more_car 获取的json
# ofset: 偏移量
def get_car_image_by_json(category, concern_id, rep_json, ofset):
    print("craw series", concern_id)
    car_file = open("data/car_infos.txt", "a", encoding='utf-8')
    while rep_json:
        if (ofset != 0) and (int(rep_json['data']['paging']['total_count']) - int(ofset) < 30):
            break
        # save info
        infos = rep_json['data']['list']
        for info in infos:
            info = info['info']
            if info.get('car_name', False):
                brand_id = str(info.get('brand_id', ""))
                series_id = str(info.get('series_id', ""))
                car_id = str(info.get('car_id', ""))
                brand_name = str(info.get('brand_name', "")).replace(' ', '')
                series_name = str(info.get('series_name', "")).replace(' ', '')
                car_name = str(info.get('car_name', "")).replace(' ', '')
                color = info.get('color', "")
                color_name = info.get('color_name', "")
                official_price = str(info.get('official_price', ""))
                toutiaothumburl = info.get('toutiaothumburl', "")
                toutiaourl = info.get('toutiaourl', "")
                year = str(info.get('year', ""))

                # car_file.writelines(",".join([brand_id, series_id, car_id, brand_name, series_name, car_name, color,
                #                               color_name, official_price, toutiaothumburl, toutiaourl, year, "\n"]))
                print(",".join([brand_id, series_id, car_id, brand_name, series_name, car_name, color,
                                color_name, official_price, toutiaothumburl, toutiaourl, year, "\n"]))
                # save_database(brand_name, car_name, color, color_name, official_price, series_id, series_name,
                #               toutiaothumburl, toutiaourl, year)
            else:
                print("not save :", info)
        ofset += 30
        rep_json = request_more_car(category, concern_id, ofset)
        time.sleep(0.25)
    car_file.flush()
    car_file.close()


def save_database(brand_name, car_name, color, color_name, price, series_id, series_name, thumburl, url, year):
    save_sql = "INSERT INTO `craw`.`dongchedi` ( " \
               "`brand_name`, `car_name`, `color`, `color_name`, `price`, `series_id`, `series_name`, `thumburl`, " \
               "`url`, `year`) VALUES ('" + brand_name + "','" + car_name + "','" + color + "', '" + color_name + \
               "', '" + price + "', '" + series_id + "', '" + series_name + "', '" + thumburl + "', '" + url + "', '" + year + "');"
    # print(save_sql)
    mysql = MysqlTool()
    mysql.execute(save_sql)


# 从懂车帝json中提取所有分类的车品牌
def generate_car_brands_txt():
    brands_file = open("data/car_brands.txt", "a", encoding='utf-8')
    with open("data/carBrand.txt", encoding='utf-8') as f:
        brand_list = json.load(f)['brands']
    for gpd_dict in brand_list:
        for brand in gpd_dict:
            if brand.get('info').get('brand_id'):
                pinyin = brand.get('info').get('pinyin', "")
                brand_id = str(brand.get('info').get('brand_id', ""))
                brand_name = brand.get('info').get('brand_name', "")
                br_info = ",".join([pinyin, brand_id, brand_name])
                brands_file.writelines(br_info + "\n")
    print("get brands done!")
    brands_file.close()


# 根据brands.txt 生成全部车型号
def generate_series_txt():
    brands_file = open("data/car_brands.txt", "r", encoding='utf-8')
    series_file = open("data/car_series.txt", "a", encoding='utf-8')
    i = 1
    while 1:
        data_line = brands_file.readline()
        if not data_line:
            break
        data = data_line.split(",")
        print("get", i, "brands ", data[2])
        i += 1
        car_se = request_car_series(data[1])
        for se in car_se:
            se_info = ",".join(
                [str(se['brand_id']), str(se['concern_id']), se['outter_name'], str(se['car_ids']).replace(',', ';')])
            series_file.writelines(se_info + "\n")
    brands_file.close()
    series_file.close()


# 根据车品牌获取车所有的型号 写入文件
def generate_car_series_by_brand(brand_id):
    series_file = open("data/car_series_by_brand_id.txt", "a", encoding='utf-8')
    car_series = request_car_series(brand_id)
    for i, se in enumerate(car_series):
        se_info = ",".join([str(i + 1), str(se['concern_id']), se['outter_name']])
        series_file.writelines(se_info + "\n")
        print("get ", i + 1)
    print("done!")
    # get_car_image_by_color('wg', car_series)


def get_car_image_from_series_txt():
    series_file = open("data/series_getting.txt", "r", encoding='utf-8')
    while 1:
        data_line = series_file.readline()
        if not data_line:
            break
        data = data_line.split(",")
        get_car_image_by_concern_id('wg', data[1], 0)
        time.sleep(1)
    series_file.close()


# 抓取时抛出异常或者被封ip， 记录下 seriesId、craw(offset) 使用此方法继续抓取
def duandian_servies():
    # eg: this series: 1646   craw: 150 total: 234
    get_car_image_by_concern_id('wg', 3634, ofset=0)


# 删除数据库中的重复数据
def delete_duplicate_data():
    du_file = open("data/duplicate_data.txt", "r")
    while 1:
        data_line = du_file.readline().replace("\n", "")
        if not data_line:
            break
        data = data_line.split("\t")
        print("delete ", data[0])
        exe_sql = "DELETE FROM dongchedi WHERE url= '" + str(data[1]) + "' AND id != " + str(data[0]) + ";"
        MysqlTool.execute(exe_sql)


def get_image_shape(img_name):
    image = io.imread(img_name)
    print(image.shape)
    print(image.dtype)


if __name__ == '__main__':
    # get_car_image_from_series_txt()
    # duandian_servies()
    # delete_duplicate_data()
    # generate_car_series_by_brand(280)
    get_image_shape('./record/A/2/96/25324_#F7F6F1_00000.jpg')
