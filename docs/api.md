# api文档

错误代码查阅 docs/error.txt

api若有出入以 apps/transfer.py 为准

# 目录

## 与客户端

* [添加用户 ./api/user/add/](#添加用户-apiuseradd)
* [查询用户 ./api/user/query/](#查询用户-apiuserquery)
* [用户关注 ./api/user/follow/](#用户关注-apiuserfollow)
* [添加处理任务 ./api/tasks/add/](#添加处理任务-apitasksadd)
* [图片信息上传（不使用七牛回调） ./api/image/addinfo/](#图片信息上传（不使用七牛回调）-apiimageaddinfo)


# 与计算端 (cpu服务器)


* [上传图片](#上传图片)
* [下载图片](#下载图片)
* [图片查询 ./api/image/query/](#图片查询-apiimagequery)

# 与客户端（WebAPP）


## 添加用户 ./api/user/add/

参数|类型或值
------------ | -------------
email|str
username|str
password|str(若要加密，在前端执行)

return

字段|类型或值
------------ | -------------
code | 1或-2


## 查询用户 ./api/user/query/

参数|类型或值
------------ | -------------
username|str
password|str(可选，获取login_bool)

suc:

字段|类型或值
------------ | -------------
code | 1
username | str
email | str
login | false
follow_user | 用户名字符串数组
followed_user | 用户名字符串数组

密码正确额外信息：

字段|类型或值
------------ | -------------
login | true
id | int

fail:

字段|类型或值
------------ | -------------
code | <1

## 用户关注 ./api/user/follow/

参数|类型或值
------------ | -------------
from_user_name|str
to_user_name|str
follow_bool|1或0（关注/取关)

return

字段|类型或值
------------ | -------------
code | 1或-1

## 图片信息上传（不使用七牛回调） ./api/image/addinfo/

参数|类型或值
------------ | -------------
url|str
filename|str
param|long_str
user_id|int

return

字段|类型或值
------------ | -------------
code | 1或-1

## 添加处理任务 ./api/tasks/add/

参数|类型或值
------------ | -------------
url |str
type |str 默认'model'
param | str 默认'mosaic'


return

字段|类型或值
------------ | -------------
code | 1

## 查看当前任务情况 ./tasks/query/ （测试用，维护中）

参数|类型或值
------------ | -------------
tasks | 任务队列
done | 完成队列



# 与计算端 (cpu服务器)

## 上传图片

使用对应七牛sdk，[下载地址](http://developer.qiniu.com/resource/official.html#sdk)。将上传图片名和回调服务器作为参数发给七牛服务器，七牛服务器上传成功后返回回调给业务处理服务器，验证后再由业务服务器返回给前端发送成功消息。

前端 => 七牛 => 后端 => 前端


参数|类型或值
------------ | -------------
access_key | iQ3ndG5uRpwdeln_gcrH3iiZ7E3KbMdJVkdYV9Im
secret_key | AGsp6K7fu1NsH2DnsPi7hW3qa3JXb4dtfeGvkm-A
bucket_name | image
bucket_domain | https://oi3qt7c8d.qnssl.com/
callbakUrl | http://139.129.24.151/api/image/upload
callbackBody | filename:$(fname)&filesize:$(fsize)&param:$(fparam)

suc:

字段|类型或值
------------ | -------------
code | 1
filename | str
url | str
param | str



## 下载图片

method: get

url = bucket_domain + filename

suc:

图片文件

fail:

{"error":"Document not found")

## 图片查询 ./api/image/query/


method:get

字段|类型
------------ | -------------
id | int

suc:

字段|类型或值
------------ | -------------
code | 1
id | int
url | str
param | str

fail:

字段|类型或值
------------ | -------------
code | <1
