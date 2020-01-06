# -*- coding:utf-8 -*-
import math
import os
import time

import requests

from dongchedi.lib import MysqlTool


def save_data(data_url, data_name, file_path, lable):
    """
    save 一个 data 到文件夹
    :param data_url: data url地址
    :param data_name: 保存data的名称，包含父级目录
    :param file_path: data 保存的根目录
    :param lable: data 分类标签
    :return: 是否成功 1 成功；-1 失败
    """
    save_failed = open("data/save_failed.txt", "a")
    saved = open("data/saved.txt", "a")
    file_path = '{}{}'.format('E:\\MyFile\\document_pycharm\\pytorch_car_classifier\\record\\images\\', file_path)
    try:
        if not os.path.exists(file_path):
            print('file ', file_path, 'not exist. building...')
            os.makedirs(file_path)
        file_suffix = os.path.splitext(data_url)[1]
        filename = '{}{}{}{}'.format(file_path, os.sep, data_name, file_suffix)
        r = requests.get(data_url)
        with open(filename, 'wb') as f:
            f.write(r.content)
        saved.writelines(",".join([filename, lable, "\n"]))
    except IOError as e:
        save_failed.flush()
        print('file save exception.', e)
        save_failed.writelines(",".join([data_name, file_path, data_url, '\n']))
        return -1
    except Exception as e:
        save_failed.flush()
        print('exception. ：', e)
        save_failed.writelines(",".join([data_name, file_path, data_url, '\n']))
        return -1

    save_failed.flush()
    saved.flush()
    save_failed.close()
    saved.close()
    return 1


def subprocess(params):
    print('[process (%s)]' % (os.getpid()))
    for j, para in enumerate(params):
        """
        filePath: sort/brandId/seriesId/
        fileName: carId_color_00001.jpg
        """
        car_id = str(para[3])
        car_color = para[4]
        if not car_id:
            car_id = "0"
        if not car_color:
            car_color = "0"
        filePath = "/".join([para[0], str(para[1]), str(para[2])])
        fileName = "".join([car_id + "_" + car_color + "_" + str(j).zfill(6)])
        url = para[5]
        lable = str(para[2])
        save_data(url, fileName, filePath, lable)
        print('[num ]', j + 1, '[sort ]', para[0], ' [name ]', fileName)
        if j + 1 % 1000 == 0:
            time.sleep(5)


def retry():
    du_file = open("data/_failed.txt", "r")
    while 1:
        data_line = du_file.readline().replace("\n", "")
        if not data_line:
            break
        data = data_line.split(",")
        save_data(data[2], str(data[0]), str(data[1]), str(0))
        print('retry ', data[0])
    du_file.close()


def generate_train_txt(uri_list, series_id):
    train_file = open("data/train.txt", "a")
    for uri in uri_list:
        train_file.writelines(uri + "," + str(series_id) + "\n")
    train_file.flush()
    train_file.close()


def generate_val_txt(uri_list, series_id):
    val_file = open("data/val.txt", "a")
    for uri in uri_list:
        val_file.writelines(uri + "," + str(series_id) + "\n")
    val_file.flush()
    val_file.close()


def get_car_id(str):
    # ./S/26/1199/34078_#000000_165707.jpg,1199,
    return str.split('/')[4].split('_')[0]


def get_lable(series_id):
    mysql = MysqlTool()
    exe_sql = "SELECT id FROM car_series WHERE series_id = '" + series_id + "';"
    return MysqlTool.execute(exe_sql)[1][0][0]


def generate_train_test_txt():
    du_file = open("data/_train.txt", "r")
    _car_id = None
    uri_lists = []
    lable = 0
    while 1:
        data_line = du_file.readline().replace("\n", "")
        if not data_line:
            break
        data = data_line.split(",")
        print(data)
        car_id = get_car_id(data[0])
        series_id = data[1]
        if not _car_id:
            _car_id = car_id
            uri_lists.append(data[0])
        else:
            if car_id == _car_id:
                uri_lists.append(data[0])
            else:
                val_uri_lists = []
                size = len(uri_lists)
                lable = get_lable(series_id)
                if size > 2:
                    val_size = math.ceil(size * 0.2)
                    for i in range(val_size):
                        val = uri_lists.pop(i + 1)
                        val_uri_lists.append(val)

                generate_train_txt(uri_lists, lable)
                generate_val_txt(val_uri_lists, lable)
                _car_id = car_id
                uri_lists = [data[0]]
    if uri_lists:
        generate_train_txt(uri_lists, lable)
    du_file.close()


if __name__ == '__main__':  # 执行主进程

    # start = 320227
    # size = 300000
    #
    # exe_sql = "SELECT sort, brand_id, series_id, car_id, color, thumb_url FROM car_info LIMIT " + str(
    #     start) + "," + str(size) + ";"
    # infos = MysqlTool.execute(exe_sql)[1]
    # subprocess(infos)
    # retry()
    generate_train_test_txt()
