# Mm131Parser

[源码地址](https://github.com/jelly54/crawler/tree/master/mm131)

## 环境

- python 3.6
- requests 2.20.0
- lxml 4.2.5

## 使用方法

1. 首先您需要拥有python 3。请自行安装，本文不涉及安装步骤。
2. 其次将文件下载到本地，目录结构如下
```
mm131
└─lib
│   └─ parser.py
├─ main.py
├─ README.md
└─ requirements.txt
```
3. 然后您需要安装上述环境中的各依赖。
```shell
root@localhost:~$ pip install -r requirements.txt
```
4. 在 mm131 目录下执行
```shell
root@localhost:~/mm131$ python main.py
```
5. 稍后您将会看到抓取过程中的输出，并在 *mm131* 文件夹中看到抓取到的picture。

![l2TCOe.png](https://upload-images.jianshu.io/upload_images/12361519-f3abced14dc6f406.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![l2TieH.png](https://upload-images.jianshu.io/upload_images/12361519-f045050bff522652.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![l2T9yD.png](https://upload-images.jianshu.io/upload_images/12361519-f4c4cf3415d7cb48.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 脚本思路

### 网站的防刷策略

> 直接访问 *http://www.mm131.net/xinggan/* 将会被强制跳转到 *index* 界面，并且内容被置为空字符串。

经过Google浏览器的F12，找到了网站的防刷策略，关建在一个叫做 *uaabc.js* 的脚本文件

```js
var mUA = navigator.userAgent.toLowerCase() + ',' + document.referrer.toLowerCase();
var _sa = ['baiduspider', 'baidu.com', 'sogou', 'sogou.com', '360spider', 'so.com', 'bingbot', 'bing.com', 'sm.cn', 'mm131.net'];
var _out = false;
for (var i = 0; i < 10; i++) {
    if (mUA.indexOf(_sa[i]) > 1) {
        _out = true;
        break
    }
}
if (!_out) {
    var _d = new Date();
    var _h = _d.getHours();
    if (_h >= 0 && _h <= 23) {
        var mPlace = escape(lo).toLowerCase();
        if (mPlace == '%u5317%u4eac%u5e02' || mPlace == '%u56db%u5ddd%u7701' || mPlace == '%u6e56%u5317%u7701') {
            top.location.href = 'https://m.mm131.net/index/';
        }
    }
};
```

脚本的大概意思是：**userAgent** 或者 **referrer** 中必须存在 **['baiduspider', 'baidu.com', 'sogou', 'sogou.com', '360spider', 'so.com', 'bingbot', 'bing.com', 'sm.cn', 'mm131.net']** 中的一个，
否则将会判断你的当前IP是否是 **[北京、湖北、四川]** 的，是的话将会强制跳转回 *index* 。

那么，我们只需要保证 **refer** 中包含 **mm131.net**，详情可见 [parser.py](https://github.com/jelly54/crawler/blob/2cf966fb313dbaf64ded98756011f725dfde0b84/mm131/lib/parser.py#L14) 中的 **set_header()** 方法。

```python
 def set_header(self, referer):
        headers = {
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': '{}'.format(self.__set_referer(referer)),
        }
        return headers
```

### 解析界面

#### 获取首页中主题ID、title

访问 [http://www.mm131.net/xinggan/](http://www.mm131.net/xinggan/) 后会获取最新的20个主题的 ID以及title，这个将会用作下一步获取主题picture。
通过lxml 的 etree 对html进行定位和解析，最终获取到 id和title。详情可见 [parser.py](https://github.com/jelly54/crawler/blob/2cf966fb313dbaf64ded98756011f725dfde0b84/mm131/lib/parser.py#L35) 中的 **_ids_titles()** 方法。

### 获取一个主题的所有picture链接

因为所有的picture链接都是很有规律的，很容易就可以拼接出某个主题的所有picture链接。详情可见 [parser.py](https://github.com/jelly54/crawler/blob/2cf966fb313dbaf64ded98756011f725dfde0b84/mm131/lib/parser.py#L59) 中的 **_ids_titles()** 方法。

### 存储

上一步已经获取到了所有的picture链接了，有了链接，接下来就是存储就好了。可以使用串行下载，当然也可以使用并行，根据自己的需要自行调整就好啦。

- 串行下载一个页面的所有主题picture。[get_page](https://github.com/jelly54/crawler/blob/2cf966fb313dbaf64ded98756011f725dfde0b84/mm131/lib/parser.py#L115)
- 并行下载一个页面的所有主题picture。[get_page_parallel](https://github.com/jelly54/crawler/blob/2cf966fb313dbaf64ded98756011f725dfde0b84/mm131/lib/parser.py#L139)

### 搜索模块

可以直接搜索想要的角色的picture进行下载。但是目前由于官网服务器内部错误，待解决。

---

# abort me

欢迎大家访问，留下你的脚印。

- github: [https://github.com/jelly54](https://github.com/jelly54)
- blog:  [https://jelly54.github.io](https://jelly54.github.io)