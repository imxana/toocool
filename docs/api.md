# 与客户端



# 与计算端

## 上传图片

使用对应七牛sdk，[下载地址](http://developer.qiniu.com/resource/official.html#sdk)。将上传图片名和回调服务器作为参数发给七牛服务器，七牛服务器上传成功后返回回调给业务处理服务器，验证后再由业务服务器返回给前端发送成功消息。

前端 => 七牛 => 后端 => 前端


参数|类型或值
------------ | -------------
'access_key' | iQ3ndG5uRpwdeln_gcrH3iiZ7E3KbMdJVkdYV9Im
'secret_key' | AGsp6K7fu1NsH2DnsPi7hW3qa3JXb4dtfeGvkm-A
'bucket_name' | image
'bucket_domain' | https://oi3qt7c8d.qnssl.com/
'callbakUrl' | http://139.129.24.151/api/image/upload
'callbackBody' | 'filename:$(fname)&filesize:$(fsize)&param:$(fparam)'

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

## 图片查询 ./api/image/query


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
