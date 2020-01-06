# coding=utf-8
import requests
from lxml import etree


# 根据名称获取到所有的相关影视，并打印到控制台


class MysqlTool:

    def __init__(self, host='localhost', port=3306, user='root', passwd='123456', db='craw', charset='utf8'):
        import pymysql
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)

    def execute(self, exe_sql):
        import time
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


def search_name_type_time_uri(url):
    rep = requests.get(url)
    uls = etree.HTML(rep.text).xpath('//div[@class="xing_vb"]/ul')
    size = len(uls)
    res = []
    for i, ul in enumerate(uls):
        if i == size - 2:
            break
        movie_name = ul.xpath('//span[@class="xing_vb4"]')[i].xpath('string(.)').strip()
        movie_type = ul.xpath('//span[@class="xing_vb5"]')[i].xpath('string(.)').strip()
        movie_time = ul.xpath('//span[@class="xing_vb6"]')[i].xpath('string(.)').strip()
        uris = url.split("/")
        detail_url = "".join([uris[0], "//", uris[2], ul.xpath('//span[@class="xing_vb4"]/a/@href')[i]])
        print(movie_name, movie_type, movie_time, detail_url)
        res.append([movie_name, movie_type, movie_time, detail_url])
    return res


# 可以手动切换detail_url，即可获取到player_url、download_url
def get_detail(detail_url):
    rep = requests.get(detail_url)
    detail_res = []
    play_uls_1 = etree.HTML(rep.text).xpath('//div[@class="vodplayinfo"]/div/ul')
    play_uls_2 = etree.HTML(rep.text).xpath('//div[@class="vodplayinfo"]/div/div/ul')

    if len(play_uls_1) < 1:
        play_uls_1 = play_uls_2
    if play_uls_1 is not None:
        for i, ul in enumerate(play_uls_1):
            print("Play source ", i + 1)
            play_url = str(ul.xpath('li/text()')).replace(",", ",\n")
            detail_res.append(play_url)
            print(play_url)
    return detail_res


# 切换不同的host即可切换不同的源
def get_url(name):
    hots = "www.zuidazy1.net"
    # hots = "www.okzyw.com"
    # hots = "www.156zy.co"   # 需要解码
    # hots = "www.mbkkk.com"
    # hots = "www.zuixinzy.cc"
    # hots = "www.subo988.com"
    # hots = "www.baiwanzy.com"
    # hots = "www.kubozy.net"
    # hots = "www.605zy.org"
    # hots = "www.doubanzy.com"
    # hots = "www.123ku.com"
    # hots = "chaojizy.com"
    # hots = "131zy.vip"
    # hots = "666zy.com"
    # hots = "maoyan123.com"

    url = "".join(["http://", hots, "/index.php?m=vod-search-pg-1-wd-", name, ".html"])
    return url


def insert_movie(movies):
    mysql = MysqlTool()
    movie_sql_pre = "INSERT INTO `craw`.`movie` (`m_name`, `m_type`, `m_detail_url`, `m_updated`) VALUES "
    movie_sql_mid = []
    for movie in movies:
        movie_sql_mid.append("('" + movie[0] + "','" + movie[1] + "','" + movie[3] + "','" + movie[2] + "')")
    mysql.execute(movie_sql_pre + ",".join(movie_sql_mid))


def insert_movie_detail(movie_name, movie_detail):
    mysql = MysqlTool()
    detail_sql_pre = "INSERT INTO `craw`.`movie_detail` (`m_name`, `m_episodes`, `m_url`) VALUES "
    detail_sql_mid = []
    for detail in movie_detail:
        down_urls = detail.encode("utf-8").replace("[", "").replace("]", "").replace("'", "").split(",\n")
        for download_url in down_urls:
            download = download_url.split("$")
            detail_sql_mid.append("('" + movie_name + "','" + download[0] + "','" + download[1] + "')")
    mysql.execute(detail_sql_pre + ",".join(detail_sql_mid))


# 查询同时向数据库中记录数据
def db_main(name):
    url = get_url(name)
    nttus = search_name_type_time_uri(url)
    insert_movie(nttus)
    for detail in nttus:
        insert_movie_detail(detail[0], get_detail(detail[3]))


def main(name):
    url = get_url(name)
    nttus = search_name_type_time_uri(url)
    get_detail(nttus[0][3])


if __name__ == '__main__':
    main("神盾局")
