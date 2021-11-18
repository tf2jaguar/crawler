from lagou.lib.parser import LaGouParser

if __name__ == '__main__':
    lg = LaGouParser()
    lg.cookie = 'edu_gate_login_token=$$$EDU_eyJraWQixx'
    lg.course_ids = '694'
    lg.save_path='./lg'
    lg.download_article = True
    lg.article2md = True
    lg.article2pdf = True
    lg.download_video = False
    lg.use_parallel = True
    lg.run()
