# crawJianShu

使用的python2.7.13，lxml，re表达式，json解析数据, MySQLdb 


爬取的起始页面为简书30日热搜，http://www.jianshu.com/trending/monthly


因为简书采用瀑布流的异步加载的方式，通过解析他发送的xhr请求，发现是请求URL的规律，当前界面的url加上当前页面已经看到的文章的id，最后在传一个”page=*“的参数。


etree获取页面数据，通过xpath解析找到每一个“li”标签，包含文章的基础信息，找到对应的文章的href，拼出每一篇文章的具体url，

article_url = 'http://www.jianshu.com' + str(info.xpath('div/a/@href')[0])


进入文章界面，xpath解析具体的数据，插入本地，MYSQL数据库


