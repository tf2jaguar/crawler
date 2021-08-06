# 拉勾教育爬虫

# 爬取视频


# 爬取文章

```
# 创建parser实例
lg = LaGouParser()
# 待抓取的课程ids
lg.course_ids = '3,9,64,59'
# 是否抓取文章为 pdf
lg.download_article = True
# 是否抓取视频
lg.download_video = False
# 是否使用多进程抓取(16)
lg.use_parallel = True
lg.run()
```