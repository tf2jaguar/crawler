from lagou.lib.parser import LaGouParser

if __name__ == '__main__':
    lg = LaGouParser()
    lg.cookie = '自己的cookie'
    lg.course_ids = '455,516,257,31,447,16,478,158,5,356,64,59,9,592,612'
    lg.download_article = True
    lg.article2md = True
    lg.article2pdf = True
    lg.download_video = False
    lg.use_parallel = True
    lg.run()
