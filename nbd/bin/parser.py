# -*- coding: UTF-8 -*-
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import schedule
from lxml import etree
from lxml.html import tostring


class Nbd:
    @staticmethod
    def news_from_title(key_words):
        url = 'http://www.nbd.com.cn/columns/3.html'
        resp = requests.get(url).text
        news_day = str(etree.HTML(resp).xpath('//div[@class="g-list-text"]/div/p/text()')[0]).strip().replace('\n', '')
        if time.strftime("%Y-%m-%d") == news_day:
            news_items = etree.HTML(resp).xpath('//div[@class="g-list-text"]/div/ul/li')
            for item in news_items:
                news_title = item.xpath('a/text()')[0]
                news_url = 'http:' + item.xpath('a/@href')[0]
                if str(news_title).startswith(key_words):
                    print(time.strftime("%H:%M:%S"), 'got info. ', news_title)
                    resp = requests.get(news_url).text
                    infos = tostring(etree.HTML(resp).xpath('//div[@class="g-articl-text"]')[0])
                    return str(infos, encoding='utf-8').replace('\r\n', '<br/>')

            print(time.strftime("%H:%M:%S"), 'not get ', key_words)
            return None
        else:
            print(time.strftime("%H:%M:%S"), 'time is expired!', news_day)
        return None

    @staticmethod
    def job(key_words):
        __html = Nbd.news_from_title(key_words)
        while not __html:
            time.sleep(30)
            __html = Nbd.news_from_title(key_words)

        mail = MailTool(mailto_list=['jelly_54@163.com'])
        mail.send_mail(sub=key_words, body=__html)


class MailTool:
    def __init__(self, mailto_list=None):
        if mailto_list is None:
            mailto_list = ['jelly_54@163.com']
        self.mailto_list = mailto_list  # 收件人(列表)
        self.mail_host = "smtp.163.com"  # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
        self.mail_user = "BigJelly54"  # 用户名
        self.mail_pass = "shouquanma963"  # 密码
        self.mail_postfix = "163.com"  # 邮箱的后缀，网易就是163.com

    def send_mail(self, sub, body, file_name=None):
        me = "Big Jelly" + "<" + self.mail_user + "@" + self.mail_postfix + ">"
        msg = MIMEMultipart()
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(self.mailto_list)
        # 添加正文
        msg.attach(MIMEText(body, 'html', 'utf-8'))

        # 添加附件
        if file_name:
            part = MIMEApplication(open(file_name, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(part)
        try:
            server = smtplib.SMTP_SSL(self.mail_host)
            server.set_debuglevel(0)
            server.ehlo(self.mail_host)
            server.login(self.mail_user, self.mail_pass)
            server.sendmail(me, self.mailto_list, msg.as_string())
            server.quit()
            print(time.strftime("%H:%M:%S"), "send mail to " + ','.join(str(to) for to in self.mailto_list) + " done.")
            return True
        except Exception as e:
            print(time.strftime("%H:%M:%S"),
                  "send mail to " + ','.join(str(to) for to in self.mailto_list) + " failed!")
            print(str(e))
            return False


def python_schedule(_time_tile_dict):
    for k, v in _time_tile_dict.items():
        schedule.every().day.at(k).do(Nbd.job, v)
    print('%s start schedule mission.\n%s' % (time.strftime("%H:%M:%S"), schedule.jobs))
    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == '__main__':
    # 方法一：使用python 内置定时任务
    time_tile_dict = {'6:00': '早财经', '12:00': '每经午时'}
    python_schedule(time_tile_dict)

    # 方法二：结合操作系统的定时任务，直接执行 job
    # Nbd.job("每经午时")
