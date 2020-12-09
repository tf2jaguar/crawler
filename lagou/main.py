# from lib.parser0 import LaGou_spider
# from lib.parser1 import LaGou_Article_Spider
from lagou.lib.parser import LaGouParser

if __name__ == '__main__':
    lg = LaGouParser()
    lg.course_ids = '3,9,64,59'
    lg.download_article = True
    lg.download_video = False
    lg.use_parallel = True
    lg.run()
