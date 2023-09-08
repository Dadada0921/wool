"""
微信阅读:小阅阅多线程并发版本，帮别人挂的最佳选择
链接:https://wai2023090606-1304279846.cos.ap-nanjing.myqcloud.com/todo.html?auth=31cf5cf7e3f49fd7ce1738ac295dcc4f&codeurl=wai2023090606-1304279846.cos.ap-nanjing.myqcloud.com&codeuserid=2&time=1694150293
抓 1692433047.3z2rpa.top 下的 cookie: ysm_uid=xxxxx,
只要xxxxxx
export xyycks='xxxxxxxx@xxxxxxxx'
如果你是让别人代挂的，你可以让代挂的给你扫一下wxpuser的码，再把uid发送给他就行
必要推送:WXPUSER  前往网站https://wxpusher.zjiecode.com/docs/#/?id=%e6%b3%a8%e5%86%8c%e5%b9%b6%e4%b8%94%e5%88%9b%e5%bb%ba%e5%ba%94%e7%94%a8
查看注册推送教程
以下推送变量
export WXPUSER_TOKEN='AT_XXXXXA...'
export WXPUSER_TOPICID='1111111'   # 这个可以不填 
export WXPUSER_UID='UID_xxxxx@UID_XXXX' WXPUSER_TOPICID和WXPUSER_UID二选一即可 WXPUSER_UID要和cookie数量一致，WXPUSER_UID可以重复填
比如我2个微信阅读只想推送给一个微信 那就export WXPUSER_UID='UID_123456@UID_123456'

前者群发，后者单推个人，推荐后者

"""

import requests
import time
import random
import os,threading
from typing import Optional, Dict 
from urllib.parse import urlparse, parse_qs,quote


class Xyy:
    def __init__(self) -> None:
        """
        """
        self.url = 'http://1692433047.3z2rpa.top/yunonline/'      
        
    def request(self, url, method='get', data=None, add_headers: Optional[Dict[str, str]] = None, headers=None):
        host = urlparse(url).netloc
        _default_headers = {
            'Host': host,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36 "
                        "MMWEBID/2651 MicroMessenger/8.0.40.2420(0x28002851) WeChat/arm64 Weixin NetType/WIFI "
                        "Language/zh_CN ABI/arm64",
            "Accept-Encoding": "gzip, deflate",
            "X-Requested-With": "com.tencent.mm",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        try:
            request_headers = headers or _default_headers
            if add_headers:
                request_headers.update(add_headers)
            
            with requests.request(method, url, headers=request_headers, data=data) as response:
                if response.status_code == 200:
                    return response.json()  # 返回JSON数据
                else:
                    print(f"请求失败状态码:{response.status_code}")
                    return None
        except Exception as e:
            # print(e)
            return None

    def account(self):
        add_header = {'Accept':'application/json, text/javascript, */*; q=0.01','cookie':self.cookie}
        ts = int(time.time()*1000)
        url = self.url + f'v1/gold?time={ts}&unionid={self.user}'
        res = self.request(url,add_headers=add_header)
        if res and res['errcode'] == 0:
            print(f"【用户{self.index}】金币:{res['data']['day_gold']}, 剩余文章{res['data']['remain_read']}")
            if res['data']['remain_read'] >0:
                print(f"【开始{self.index}】:获取开篇文章url")
                time.sleep(3)
                urla = self.start()
                self.request(urla)
                host = urlparse(urla).netloc
                query_parameters = parse_qs(urlparse(urla).query)
                uk = query_parameters.get('uk', [])[0] if query_parameters.get('uk') else None
                if uk:
                    for i in range(1,res['data']['remain_read']+1):
                        print(f"【阅读{self.index}】:第{i}篇文章！")
                        self.do_read_task(host,uk=uk)
                        if self.cont == False:
                            break
                        time.sleep(random.randint(1,3))
                else:
                    print("没有发现uk")
            else:
                print(f"没有可阅读的文章了")
        else:
            print(f"出错了:{res}")
    
    def start(self):
        url = 'http://1692435610.3z2rpa.top/yunonline/v1/wtmpdomain'
        data = f'unionid={self.user}'
        add_headers = {"Content-Lenght": str(len(data)),"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","Origin":"http://1692435610.3z2rpa.top","Referer":"http://1692435610.3z2rpa.top/?cate=0"}
        res = self.request(url,'post',data=data, add_headers=add_headers)
        if res['errcode'] == 0:
            print(f"【文章{self.index}】: url加载成功")
            return res['data']['domain']
        else:
            return None

    
    def do_read_task(self,origin,uk):
        url = f'https://nsr.zsf2023e458.cloud/yunonline/v1/do_read?uk={uk}'
        add_header= {'origin': f'https://{origin}','accept':'application/json, text/javascript, */*; q=0.01','sec-fetch-site':'cross-site'}
        res = self.request(url,add_headers=add_header)
        if res:
            if res['errcode'] == 0:
                link_url = res['data']['link']
                time.sleep(random.randint(2,4))
                self.jump(url=link_url,uk=uk)
                # ts = random.randint(7,15)
                # print(f"【等待{self.index}】:休息{ts}秒")
                # time.sleep(ts)
                # self.complete_task(uk,ts)
            else:
                print(f"【阅读{self.index}】:{res['msg']}")
                if res['errcode'] == 407:
                    self.cont = False
        else:
            print("发生了点意外,休息3秒")
            time.sleep(3)
            self.do_read_task(origin,uk)

    def complete_task(self,uk,ts):
        tsp = int(time.time())*1000
        url = f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={uk}&time={ts}&timestamp={tsp}'
        res = self.request(url)
        if res and res['errcode'] == 0:
            print(f"【奖励{self.index}】:{res['msg']}, +{res['data']['gold']}币,今天阅读数:{res['data']['day_read']},剩余{res['data']['remain_read']}")
            if res['data']['gold'] == 0:
                self.cont = False
        else:
            print(f"领取阅读币失败:{res['msg']}")
            if res['errcode'] == 407:
                self.cont = False

    def jump(self,url,uk):
        url = url+'?/'
        host = urlparse(url).netloc
        headers = {
            "Host":host,
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36 MMWEBID/2651 MicroMessenger/8.0.40.2420(0x28002851) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding":"gzip, deflate",
            "X-Requested-With":"com.tencent.mm",
            "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding":"gzip, deflate",
            'Cookie': 'ysm_uid='+self.user
        }
        res = requests.get(url,headers=headers,allow_redirects=False)
        location= res.headers.get('Location')
        if self.varification(location):
            ts = random.randint(7,15)
            print(f"【等待{self.index}】:休息{ts}秒")
            time.sleep(ts)
            self.complete_task(uk,ts)

    
    def varification(self,url):
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        if '__biz' in query_parameters:
            biz_value = query_parameters['__biz'][0]
            if biz_value in self.check_data:
                print(f"【检测{self.index}】: {self.check_data[biz_value][0]} 公众号")
                encoded_url = quote(url)
                self.wxpuser("小阅阅检测,请1分钟内点击阅读",encoded_url)
                print(f"【等待{self.index}】:请手动前往wxpuser点击阅读")
                for i in range(1,61):
                    if self.get_read_state():
                        print(f"【阅读{self.index}】:已手动阅读,休息5秒继续干活")
                        time.sleep(5)
                        return True
                    if i == 59:
                        print("超时未阅读，终止本次阅读")
                        self.cont = False
                        return False
                    time.sleep(1)
            else:
                print(f"【文章{self.index}】:没有检测")
                return True
        else:
            print("__biz parameter not found in the URL")
            return True

    def check_read(self):
        url = self.aol + f'/check_dict?user={self.user}&value=0'
        res = self.request(url)
        if res and res['status'] == 200:
            self.check_data = res['check_dict']
        else:
            print(f"索取字典出现错误:{res}")
    
    def get_read_state(self):
        url = self.aol+ f'/read/state?user={self.user}&value=0'
        res = requests.get(url).json()
        if res['status'] == True:
            return True
        else:
            return False

    def wxpuser(self,title,url):
        # 此处代码抄袭了别人html的代码，见谅
        content = '''<!DOCTYPE html>
                <html lang="zh-CN">
                <head>
                <meta charset="UTF-8">
                <title>TITLE</title>
                <style type=text/css>
                    body {
                        background-image: linear-gradient(120deg, #fdfbfb 0%, #a5d0e5 100%);
                        background-size: 300%;
                        animation: bgAnimation 6s linear infinite;
                    }
                    @keyframes bgAnimation {
                        0% {background-position: 0% 50%;}
                        50% {background-position: 100% 50%;}
                        100% {background-position: 0% 50%;}
                    }
                </style>
                </head>
                <body>
                    <p>小阅阅阅读检测</p><br>
                    <p><a href="self.aol/redirect?user=abc&value=0&timestamp=1900&wxurl=link">点击阅读检测文章</a></p><br>
                </body>
            </html>
        '''
        content = content.replace('self.aol',self.aol).replace('link',url).replace('abc',self.user).replace('1900',str(int(time.time())))
        data = {
            "appToken": self.app_token,
            "content": content,
            "summary": title,
            "contentType": 2,
        }
        if self.topicid is not None:
            data["topicIds"] = [int(self.topicid)]
        if self.wx_uid is not None:
            data["uids"] = [self.wx_uid]
        # print(content)
        wxpuser_url = 'http://wxpusher.zjiecode.com/api/send/message'
        res = requests.post(wxpuser_url, json=data).json()
        if res['success'] == True:
            print(f"【通知{self.index}】:检测发送成功！")
        else:
            print(f"【通知{self.index}】:发送失败！！！！！")

    def user_gold(self):
        add_header = {'Accept':'application/json, text/javascript, */*; q=0.01','cookie':self.cookie}
        ts = int(time.time()*1000)
        url = self.url + f'v1/gold?time={ts}&unionid={self.user}'
        res = self.request(url,add_headers=add_header)
        if res['errcode'] == 0:
            current_gold = res['data']['last_gold']
            print(f"【余额{self.index}】:{current_gold}金币")
            tag = 8000
            if int(current_gold) >= tag:
                self.gold = int(int(current_gold)/1000)*1000
                self.get_requestsid()
            else:
                print(f"【余额{self.index}】:{current_gold} < {tag} ,不满足条件")
        else:
            print("出现一些问题")
        
    def get_requestsid(self):
        headers = {
            'Host': '1692416143.3z2rpa.top',
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36 "
                        "MMWEBID/2651 MicroMessenger/8.0.40.2420(0x28002851) WeChat/arm64 Weixin NetType/WIFI "
                        "Language/zh_CN ABI/arm64",
            "Accept-Encoding": "gzip, deflate",
            "X-Requested-With": "com.tencent.mm",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            'Cookie': self.cookie
        }
        res = requests.get('http://1692416143.3z2rpa.top/',headers=headers).text
        import re
        pattern = r'href="(http://[^"]+)"'
        match = re.search(pattern, res)
        if match:
            url = match.group(1)
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            request_id = query_params.get("request_id", [""])[0]
            print("request_id:", request_id)
            self.with_draw(req_id=request_id,url=url)
        else:
            print("No URL found")
    
    def with_draw(self,req_id,url):
        url1 = self.url + "v1/user_gold"
        host = urlparse(url).netloc
        data1 = f"unionid={self.user}&request_id={req_id}&gold={self.gold}"
        add_headers = {"Content-Lenght": str(len(data1)),"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","Origin":f"http://{host}","Referer":url,'Cookie':self.cookie}
        res = self.request(url1,'post',data=data1,add_headers=add_headers)
        if res['errcode'] == 0:
            print(f"【提现{self.index}】:{res['data']['money']}元")
            url2 = self.url+'v1/withdraw'
            data2 = f"unionid={self.user}&signid={req_id}&ua=2&ptype=0&paccount=&pname="
            {"Content-Lenght": str(len(data2)),"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","Origin":f"http://{host}","Referer":url,'Cookie':self.cookie}
            res = self.request(url2,'post', data=data2,add_headers=add_headers)
            if res['errcode'] == 0:
                print(f"【提现{self.index}】:{res['msg']}")
            else:
                print(f"提现失败 原因:{res['msg']}")
        else:
            print(res)
    
    def run(self, ck,app_token, wx_uid,topicid,index,url):
        self.aol = url
        self.index = index
        print(f"【开始{index}】: 第{index}个的账号")
        self.cont = True
        self.user = ck
        self.topicid = topicid
        self.app_token = app_token
        self.wx_uid = wx_uid
        self.cookie = f'ysm_uid={ck}'
        self.check_read()
        self.account()
        self.user_gold()
        print(f"【结束{index}】: cookie为 {index} 账号")


def check_env():
        wxpuser_token = os.getenv("WXPUSER_TOKEN")
        topicid = os.getenv("WXPUSER_TOPICID")
        wxpuser_uid = os.getenv("WXPUSER_UID")
        cks = os.getenv('xyycks')
        cks = 'oZdBp0x2Y9UeGNBKxUA9Ej4DtXv0@oZdBp02-aXLn3CQOLFbWxH33LAhw'
        # cks = 'oZdBp0zncuzTjN4KzFeUtqUZKB2c@oZdBp039ZVdkAnaZ39dAKhM4qahs'
        if cks is None:
            print("小悦悦ck为空，请去抓包格式:'oZdBp.....' 多账户请用@分割")
            exit()
        if wxpuser_token is None:
            print("wxpuser的apptoken为空，前往官网注册创建一个app")
            exit()
        if topicid is None and wxpuser_uid is None:
            print("wxpuser的topicid和WXPUSER_UID都为空，请至少填写其中一个")
            exit()
        return wxpuser_token, topicid, wxpuser_uid.split('@'), cks.split("@")


def test_api(url):
    print("开始测试检测服务可用性")
    api_url = url + '/read/announcement'
    res = requests.get(api_url)
    if res.status_code == 200:
        result = res.json()
        print(f"【公告】:{result['messages']}")
        return True
    else:
        return False


def main():
    apptoken, topicid, wx_uids, cks_list = check_env()  #这里顺序不能搞乱了
    aol = []
    for url in ['http://api.doudoudou.fun','http://api.hwayla.top']:
        if test_api(url):
            print(f"{url} 联通性测试通过")
            aol.append(url)
    from random import choice
    threads = []
    for ck in cks_list:
        xyy = Xyy()
        thread = threading.Thread(target=xyy.run, args=(ck,apptoken,wx_uids[cks_list.index(ck)],topicid,cks_list.index(ck)+1,choice(aol)))
        threads.append(thread)
    for thread in threads:
        thread.start()
    # 等待线程完成
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()