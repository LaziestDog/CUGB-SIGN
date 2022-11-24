# coding:utf-8
import re
import json
import time
import esprima
import requests
from bs4 import BeautifulSoup


cookies = {}
session = requests.session()
f = open('config.json', 'r', encoding='utf-8')
config = f.read()
f.close()
config = json.loads(config)

loginurl = 'https://cas.cugb.edu.cn/login'
uidgeturl = 'https://stu.cugb.edu.cn/'
uidurl = 'https://stu.cugb.edu.cn:443/caswisedu/login.htm'
checkurl = 'http://stu.cugb.edu.cn/webApp/xuegong/index.html#/zizhu/apply?projectId=4a4ce9d6725c1d4001725e38fbdb07cd&type=YQSJCJ'
posturl = 'https://stu.cugb.edu.cn:443/syt/zzapply/operation.htm'
FTurl = 'https://sctapi.ftqq.com/{}.send'
QYWXtokenurl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'
QYWXposturl ='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'
TGurl = 'https://{}/bot{}/sendMessage'
PROXYurl = '{}://{}:{}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4230.1 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

requests.packages.urllib3.disable_warnings()

try:
    req = session.request('GET', loginurl).content
    soup = BeautifulSoup(req, 'html.parser')
    execution = soup.findAll("input", {"name": "execution"})[0]["value"]
    system = soup.findAll("input", {"id": "userLoginSystem"})[0]["value"]
    uname = config['username']
    upwd = config['password']
    data = {'username': uname,
            'password': upwd,
            'execution': execution,
            '_eventId': 'submit',
            'geolocation': '',
            'loginType': 'username',
            'system': system,
            'enableCaptcha': 'N'}
    req = session.post(loginurl, data=data, headers=headers)
    cookies = requests.utils.dict_from_cookiejar(req.cookies)
    # time.sleep(3)
    req = session.request('GET', uidgeturl, cookies=cookies, headers=headers).content
    soup = BeautifulSoup(req, 'html.parser')
    scriptTags = str(soup.findAll('script')[1])
    rexp = re.compile(r'<[^>]+>', re.S)
    scriptCode = rexp.sub('', scriptTags)
    uid = esprima.tokenize(scriptCode)[48].value.replace('\'', '')
    uiddata = {'uid': uid}
    req = session.request('POST', uidurl, data=uiddata)
    # time.sleep(3)
    content = session.post(checkurl)
    if content.status_code == 200:
        desp = "Login status: Succeeded\n"
        # time.sleep(3)
    else:
        desp = "Login status: Failed\n"
    data = {
        'data': str(config["data"]).replace("'", '"' ),
        'msgUrl': '''syt/zzapply/list.htm?type=YQSJCJ&xmid=4a4ce9d6725c1d4001725e38fbdb07cd''',
        'uploadFileStr': '''{}''', 'multiSelectData': '''{}'''}
    r = session.request('POST', posturl, headers=headers, cookies=cookies, data=data)
    if r.text == 'success':
        desp += 'Clocking-in status: Succeeded\n'
        subj = '☛已提交每日健康信息...'
        content = """
        ✔今日打卡成功！
        """
    elif r.text == 'Applied today':
        desp += 'Clocking-in status: Applied today\n'
        subj = '☛健康信息今日已提交！'
        content = """
        ⚠已经打卡啦！
        """
    else:
        desp += 'Clocking-in status: Failed. Please check it\n'
        subj = '☛出现异常，请查看日志！'
        content = subj
except Exception as e:
    error = 'Error Code 1: ' + str(e)
    subj = '☛出现异常，请查看日志！'
    content = """
            【⚠警告！抛出异常代码！⚠】
            %s
            """ % error

try:
    url = FTurl.format(config["FTkey"])
    data = {
        "title": subj,
        "desp": content
            }
    requests.post(url, data=data).json()


    tokenurl=QYWXtokenurl.format(config["QYWXid"],config["QYWXsecret"])
    getr = requests.get(tokenurl)
    access_token = getr.json().get('access_token')
    tmptext = "<div class=\"gray\">" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "</div> <div class=\"normal\">" + subj + "</div><div class=\"highlight\">" + content + "</div>"
    data =     {
       "touser" : "@all",
       "msgtype" : "textcard",
       "agentid" : config["QYWXbotid"],
       "textcard" : {
                "title" : "打卡通知",
                "description" : tmptext,
                "url" : "URL",
                "btntxt":"点我干嘛"
       },
       "enable_id_trans": 0,
       "enable_duplicate_check": 1,
       "duplicate_check_interval": 1800
    }
    posturl = QYWXposturl.format(access_token)
    requests.post(posturl, data=json.dumps(data))


    url = TGurl.format(config["TGurl"], config["TGtoken"])
    data = {
        'chat_id': config["TGID"],
        'text': f'#健康信息提交\n{subj}\n{content}',
        'disable_web_page_preview': 'true'
            }
    proxyurl = PROXYurl.format(config["PROXY"],config["PROXYip"],config["PROXYport"])
    proxies={
        'http':proxyurl,
        'https':proxyurl
        }
    requests.post(url, data=data, proxies=proxies, timeout=15).json()
except Exception as e:
    exit()    
