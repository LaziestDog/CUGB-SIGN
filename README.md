# CUGB-SIGN
![](https://visitor-badge.glitch.me/badge?page_id=LaziestDog.CUGB-SIGN )

An automatic python script for CUGB's COVID-19 report  
中国地质大学（北京）疫情期间每日自动进行健康打卡上报  
***免责声明（Disclaimer）：使用该脚本而可能引起的法律责任和学校追究等责任由使用者个人承担，与开发者无关，请勿滥用。为了您和他人的健康着想，请如实填写信息，在有位置变动和情况变化时手动填写申报！***

## 使用方法

> **必须环境 python3**

### 配置环境

```
git clone https://github.com/LaziestDog/CUGB-SIGN.git
git clone https://ghproxy.com/https://github.com/LaziestDog/CUGB-SIGN.git #国内速度太慢请用这条拉取
pip3 install esprima requests
cd CUGB-SIGN
cp config.example.json config.json
```

#### 填写参数

打开`config.json`文件

##### 个人信息

```
"username":"123456",//学号
"password":"123456",//密码
```

##### 签到信息

> 个人建议抓包一次然后自行替换

```
"data":{
        "xmqkb":{"id":"4a4ce9d6725c1d4001725e38fbdb07cd"},
        "c1":"37.2℃及以下",
        "c2":"健康",
        "c17":"否",
        "c4":"否",
        "c7":"否",
        "c9":"否",
        "c6":"否",
        "c5":"否",
        "type":"YQSJCJ",
        "location_longitude":"116.37951",//不在学校请把这个改了，如有问题自负
        "location_latitude":"39.594672",//不在学校请把这个改了，如有问题自负
        "location_address":"北京市海淀区学院路街道中国地质大学(北京)"//不在学校请把这个改了，如有问题自负
        },
```

##### 信息推送

> 可填可不填，仅仅起通知作用
> 目前没有写单独推送，配置几个推送几个
> 以后再写具体申请教程

```
"FTkey": "", // 方糖key 在sc.ftqq.com申请
"TGtoken": "",//你的TG机器人的bottoken，在@botfather内申请
"TGID": "",//你的TG账号的ID
"QYWXsecret": "",//你的企业微信程序的密钥
"QYWXid": "",//你的企业的ID
"QYWXbotid": "1000002",//你的企业程序的ID
"PROXY": "http",//代理 socks5/http(TG推送所需)
"PROXYip": "127.0.0.1",//代理ip
"PROXYport": "7890"//代理端口
```



### 单次使用

```
cd CUGB-SIGN
python3 cugbsign.py
```

### 定时任务(LINUX)

* `crontab -e`

* 按`i`键

* 加入新行 `10 0 * * * python3 /root/CUGB-SIGN/cugbsign.py`

>`/root/CUGB-SIGN/cugbsign.py`改为你的目录

* 按`ESC` 输入`:wq`退出crontab编辑页面


## TO DO

- [x] 方糖气球推送
- [x] 企业微信推送
- [x] TGbot推送及其代理
- [ ] bark推送
- [ ] 优化代码(try)
- [ ] 推送设定为可自选(使用函数)
- [ ] 编写推送相关申请教程



## 致谢

Some core code is from [hanrc97](https://github.com/hanrc97/FucknCoVReport)
