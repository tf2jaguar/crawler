# -*- coding: utf-8 -*-
import json
import time

import requests
from skimage import io

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


def request_more_img(category, series_id, offset):
    url = 'https://www.dcdapp.com/motor/car_page/v3/get_picture/?version_code=445&category=' + str(category) + \
          '&series_id=' + str(series_id) + '&offset=' + str(offset) + '&car_id=null'
    # print(url)
    car_request_filed = open("../data/_request_filed.txt", "a", encoding='utf-8')
    time.sleep(0.25)
    rep = requests.get(url=url, headers=header)
    rep_json = json.loads(rep.text)
    if rep_json['status'] == 0:
        if not rep_json.get('data').get('paging'):
            rep_json = request_more_img(category, series_id, offset)
        if not rep_json:
            print("try exception!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            car_request_filed.writelines(",".join([category, str(series_id), str(offset), "\n"]))
            return None
        print("[series]:{} [craw]:{} [total]:{}".format(series_id, rep_json['data']['paging']['offset'],
                                                        rep_json['data']['paging']['total_count']))
        return rep_json
    else:
        car_request_filed.writelines(",".join([category, series_id, offset, "\n"]))
        raise Exception("get car series has exception!")


def get_car_image_by_series(category, series):
    """
    按照车系列 获取所有的车image。# offset:
    :param category: 查询分类  wg
    :param series:  车所有型号
    :return:
    """
    for i, car_se in enumerate(series):
        get_car_image_by_concern_id(category, car_se['concern_id'], 0)


def get_car_image_by_concern_id(category, concern_id, offset):
    """
    根据车ID 获取具体某一个车image信息
    :param category: 查询分类  wg
    :param concern_id: 车ID
    :param offset: 0~n  从0开始每次加30  paging:中有描述是否还有更多
    :return:
    """
    rep_json = request_more_img(category, concern_id, offset)
    __parsing_car_image_json(category, concern_id, rep_json, offset)


def __parsing_car_image_json(category, concern_id, rep_json, offset):
    """
    解析具体某一个车的image json
    :param category: 查询分类  wg
    :param concern_id: 车ID
    :param rep_json: @request_more_car 获取的json
    :param offset: 偏移量
    :return:
    """
    print("craw series", concern_id)
    car_file = open("../data/car_infos.txt", "a", encoding='utf-8')
    count = 6
    while rep_json:
        if (offset != 0) and (int(rep_json['data']['paging']['total_count']) - int(offset) < 30):
            break
        # save info
        infos = rep_json['data']['list']
        for info in infos:
            info = info['info']
            if info.get('title', False):
                count = 6
                print("craw ", info)
            elif info.get('car_name', False) and count > 0:
                brand_id = str(info.get('brand_id', ""))
                series_id = str(info.get('series_id', ""))
                car_id = str(info.get('car_id', ""))
                brand_name = str(info.get('brand_name', "")).replace(' ', '')
                series_name = str(info.get('series_name', "")).replace(' ', '')
                car_name = str(info.get('car_name', "")).replace(' ', '')
                color = info.get('color', "")
                color_name = info.get('color_name', "")
                year = str(info.get('year', ""))
                official_price = str(info.get('official_price', ""))
                toutiaothumburl = info.get('toutiaothumburl', "")
                toutiaourl = info.get('toutiaourl', "")

                car_file.writelines(",".join([brand_id, series_id, car_id, brand_name, series_name, car_name, color,
                                              color_name, official_price, toutiaothumburl, toutiaourl, year, "\n"]))
                # print(",".join([brand_id, series_id, car_id, brand_name, series_name, car_name, color,
                #                 color_name, official_price, toutiaothumburl, toutiaourl, year, "\n"]))
                count = count - 1
        offset += 30
        rep_json = request_more_img(category, concern_id, offset)
        time.sleep(0.25)
    car_file.flush()
    car_file.close()


def generate_brands_txt():
    """
    准备工作：01. 从懂车帝json中提取所有分类的车品牌
    :return:
    """
    brands_file = open("../data/_brands.txt", "a", encoding='utf-8')
    with open("../data/car_brands.json", encoding='utf-8') as f:
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


def generate_series_txt():
    """
    准备工作：02. 根据 _brands.txt 生成全部车 系列号
    :return:
    """
    brands_file = open("../data/_brands.txt", "r", encoding='utf-8')
    series_file = open("../data/_series.txt", "a", encoding='utf-8')
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


def generate_car_image_from_series_txt():
    """
    从序列中开始抓取图片
    :return:
    """
    series_file = open("../data/_series.txt", "r", encoding='utf-8')
    while 1:
        data_line = series_file.readline()
        if not data_line:
            break
        data = data_line.split(",")
        get_car_image_by_concern_id('wg', data[1], 0)
        time.sleep(1)
    series_file.close()


# 抓取时抛出异常或者被封ip， 记录下 seriesId、craw(offset) 使用此方法继续抓取
def resume_service(series_id, offset):
    flag = False
    series_file = open("../data/_series.txt", "r", encoding='utf-8')
    while 1:
        data_line = series_file.readline()
        if not data_line:
            break
        data = data_line.split(",")
        # 找到上次下载的地方
        if flag:
            get_car_image_by_concern_id('wg', data[1], 0)
            time.sleep(1)
        else:
            if int(data[1]) == series_id:
                flag = True
                print("find last position. series_id:{} offset:{}".format(data[1], offset))
                get_car_image_by_concern_id('wg', series_id, offset)

    series_file.close()


def get_image_shape(img_name):
    image = io.imread(img_name)
    print(image.shape)
    print(image.dtype)


if __name__ == '__main__':
    generate_brands_txt()
    # generate_series_txt()
    generate_car_image_from_series_txt()
    # resume_service(series_id=2673, offset=0)
    # get_image_shape('./record/A/2/96/25324_#F7F6F1_00000.jpg')
