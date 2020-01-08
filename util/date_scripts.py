#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author : Jelly
# @Date : 2020/1/7 12:53
import calendar
import datetime


def get_between_day(begin_date, end_date):
    """
    获取两个日期之间的每一天
    :param begin_date:  起始时间
    :param end_date: 结束时间
    :return:
    """
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


def get_between_month(begin_date, end_date):
    """
    获取两日期之间的每一个月
    :param begin_date:  起始时间
    :param end_date:  结束时间
    :return:
    """
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m")
        date_list.append(date_str)
        begin_date = _add_months(begin_date, 1)
    return date_list


def _add_months(dt, months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)

# linkdoc 重新跑dashboard统计
# def re_back(begin_date='2019-12-01', end_date='2020-01-07'):
#     begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
#     end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
#     print(begin_date, end_date)
#     while begin_date < end_date:
#         next_date = begin_date + datetime.timedelta(days=1)
#
#         statistics = IndicesStatistics(from_time=begin_date, to_time=next_date)
#         statistics(save=True)
#
#         begin_date = next_date
