# 必应壁纸爬虫

每天定时下载必应的图片，并替换mac book pro 的桌面壁纸


## 使用 

1. 查看 crontab 是否启动（非必要，可跳过）
```
sudo launchctl list | grep cron
```

2. 命令行创建crontab执行文件"testing_crontab"

```
vi testing_crontab
```
输入以下代码
```
*/1 * * * * /bin/date >> /Users/xx/time.txt
```
esc，wq!保存

以上代码是每分钟执行一次date命令，输出时间到time.txt文本

3. 使用crontab命令调用crontab文件

```
crontab testing_crontab
```

4. 查看当前有哪些在用的 cron 任务

```

```

5. 删除任务

进入编辑模式,  删除不需要的任务
```
crontab -e 
```


# cron 用法

## 主要用法

```
#  安装crontab
yum install crontabs

# 服务操作说明：
# 启动服务
/sbin/service crond start 

# 关闭服务
/sbin/service crond stop 

#  重启服务
/sbin/service crond restart 

#  重新载入配置
/sbin/service crond reload

#  查看crontab服务状态：
service crond status

# 手动启动crontab服务：
service crond start

# 查看crontab服务是否已设置为开机启动，执行命令：
ntsysv

# 加入开机自动启动：
chkconfig –level 35 crond on
```

## crontab命令详解

1．命令格式：

```
crontab [-u user] file

crontab [-u user] [ -e | -l | -r ]
```

2．命令功能：

通过crontab 命令，我们可以在固定的间隔时间执行指定的系统指令或 shell script脚本。时间间隔的单位可以是分钟、小时、日、月、周及以上的任意组合。
这个命令非常设合周期性的日志分析或数据备份等工作。

3．命令参数：

```
-u user：用来设定某个用户的crontab服务，例如，“-u ixdba”表示设定ixdba用户的crontab服务，此参数一般有root用户来运行。

file：file是命令文件的名字,表示将file做为crontab的任务列表文件并载入crontab。如果在命令行中没有指定这个文件，crontab命令将接受标准输入（键盘）上键入的命令，并将它们载入crontab。

-e：编辑某个用户的crontab文件内容。如果不指定用户，则表示编辑当前用户的crontab文件。

-l：显示某个用户的crontab文件内容，如果不指定用户，则表示显示当前用户的crontab文件内容。

-r：从/var/spool/cron目录中删除某个用户的crontab文件，如果不指定用户，则默认删除当前用户的crontab文件。

-i：在删除用户的crontab文件时给确认提示。
```