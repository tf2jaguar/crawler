# 拉勾教育爬虫

# 结果展示

![iShot2021-08-07 10.47.48.png](https://upload-images.jianshu.io/upload_images/12361519-e373043548281963.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 爬取文章

启动入口 [main.py](main.py) 的 main 方法

```
# 创建parser实例
lg = LaGouParser()
# 待抓取的课程ids
lg.course_ids = '3,9,64,59'
# 是否抓取文章
lg.download_article = True
# 是否将文章保存为markdown
lg.article2md = True
# 是否将文章保存为pdf
lg.article2pdf = True
# 是否抓取视频
lg.download_video = False
# 是否使用多进程抓取(16)
lg.use_parallel = True
lg.run()
```

# 爬取视频

