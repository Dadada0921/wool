"""
微信阅读:花花阅读
链接:http://mr1696919260644.ofzgcds.cn/user/index.html?mid=5K7YPZ3WC
多账号@分割
un:1111; token:2222
export hhydcks='11111&2222@xxx&xxx'
export multi_hhyd='true'  # 并发开关，可以不填
new Env('花花阅读')
"""


import asyncio
import aiohttp
import hashlib
import random,json
from typing import Optional, Dict 
from urllib.parse import urlparse,parse_qs,quote
import time,re
import os



class Hhyd:
    def __init__(self) -> None:
        self.sessions = aiohttp.ClientSession()
        self.url = 'http://u.cocozx.cn/api'

    async def close(self):
        await self.sessions.close()

    async def request(self,url,method='get',data=None, add_headers: Optional[Dict[str,str]]=None, headers=None):
        host = urlparse(url).netloc
        # self._default_headers['Host'] = host
        _default_headers={
            'Host': host,
            'Connection': 'keep-alive',
            'Content-Length': str(len(data)),
            'Accept': 'application/json, text/javascript, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue',
            'Content-Type':'application/json;charset=utf-8',
            'X-Requested-With': 'com.tencent.mm',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
            
        }
        try:
            request_headers = headers or _default_headers
            if add_headers:
                request_headers.update(add_headers)
            async with getattr(self.sessions, method)(url,headers = request_headers, data=data) as response:
                    if response.status == 200:
                        return await response.json()     #返回text或json 看情况如json就response.json()
                    else:
                        print(f"请求失败状态码:{response.status}")
                        return await response.json()    # 同理由可得
        except Exception as e:
            print(e)
            return None
    
    async def do_read_task(self):
        await asyncio.sleep(random.randint(2,5))
        for i in range(1,31):
            print(f"【用户{self.index}】【阅读】:开始第{i}次阅读")
            if await self.read():
                random_sleep = random.randint(8,15)
                print(f"【用户{self.index}】【等待】:{random_sleep}秒")
                await asyncio.sleep(random_sleep)
                await self.submit()
            else:
                break

    async def submit(self):
        url = "http://u.cocozx.cn/api/user/submit?zx=?&xz=1"
        data={
            'type':'1',
            'un':self.un,
            'token':self.token,
            'pageSize':20
        }
        res = await self.request(url,'post',data=json.dumps(data))
        if res:
            if res['code'] == 0:
                if res['result'] is not None:
                    print(f"【用户{self.index}】【奖励】:花花+{res['result']['val']}  本轮剩余{res['result']['progress']}篇")
                      
                else:
                    print(f"【用户{self.index}】【错误】:可能号黑了")
                    return False
            else:
                print(f"【用户{self.index}】【错误】:未知错误")
        else:
            print("请求出现了问题，稍后再来看吧")

    async def read(self):
        url = "http://u.cocozx.cn/api/user/read"
        data={
            'un':self.un,
            'token':self.token,
            'pageSize':20
        }
        res = await self.request(url,'post',data=json.dumps(data))
        if res:
            if res['code'] == 0:
                if res['result'] is not None:
                    if res['result']['status']==10:   
                        return True
                    elif res['result']['status']==60:
                        print(f"【用户{self.index}】【阅读状态】:今日文章全部读完")
                        return False
                    elif res['result']['status']==70:
                        print(f"【用户{self.index}】【阅读状态】:下一批文章##分钟后")
                        return False
                    elif res['result']['status']==50 or res['result']['status']==80:
                        print(f"【用户{self.index}】【阅读状态】:阅读无效，下回再来")
                        return False
                    elif res['result']['status']==30 or res['result']['status']==40:
                        print(f"【用户{self.index}】【阅读状态】:休息一会儿再来")
                        return False
                    else:
                        print(f"【用户{self.index}】【阅读状态】:未知状态{res}")
                        return False
                else:
                    print(f"【用户{self.index}】【错误】:可能号黑了")
                    return False
            else:
                print(f"【用户{self.index}】【错误】:未知错误{res}")
        else:
            print("请求出现了问题，稍后再来看吧")


    async def ustr(self,t):
        url = "http://u.cocozx.cn/api/common/ustr?t="+t
        data={
            'un':None,
            'token':None,
            'pageSize':20
        }
        res = await self.request(url,'post',data=json.dumps(data))
        if res:
            if res['code'] == 0:
                if res['result']['str']:
                    print(f"【用户{self.index}】:获取阅读地址成功{res['result']['str']}")             
            else:
                print(f"【用户{self.index}】【错误】:获取阅读地址失败")
        else:
            print("请求出现了问题，稍后再来看吧")


    async def get_read_host(self):
        url = "http://u.cocozx.cn/api/user/getReadHost"
        data={
            'un':self.un,
            'token':self.token,
            'pageSize':20
        }
        
        res = await self.request(url,'post',data=json.dumps(data))
        if res:
            if res['code'] == 0:
                if res['result']['host']:
                    print(f"【用户{self.index}】:获取阅读地址成功{res['result']['host']}")
                    host=res['result']['host']
                    t=host[9:18]
                    await self.ustr(t=t)
            else:
                print(f"【用户{self.index}】【错误】:获取阅读地址失败")
        else:
            print("请求出现了问题，稍后再来看吧")
    
    
    async def user_info(self):
        url = self.url+"user/info"
        data={
            'un':self.un,
            'token':self.token,
            'pageSize':20
        }
        res = await self.request(url,'post',data=json.dumps(data))
        if res:
            if res['code'] == 0:
                if res['result']['us']==1:
                    print(f"【用户{self.index}】【账号状态】:账号正常")
                    print(f"【用户{self.index}】【信息】:进度:{res['result']['dayCount']}/{res['result']['dayCount']+res['result']['leftCount']}   余额:{res['result']['moneyCurrent']}")
                    if res['result']['hopeNull'] is not None:
                        if res['result']['hopeNull']['status']==60:
                            print(f"【用户{self.index}】【阅读状态】:今日文章全部读完")
                        elif res['result']['hopeNull']['status']==70:
                            print(f"【用户{self.index}】【阅读状态】:下一批文章XX分钟后")
                        elif res['result']['hopeNull']['status']==50 or hopeNull.status==80:
                            print(f"【用户{self.index}】【阅读状态】:阅读无效，下回再来")
                        elif res['result']['hopeNull']['status']==30:
                            print(f"【用户{self.index}】【阅读状态】:一会儿再来看看")
                        elif res['result']['hopeNull']['status']==40:
                            print(f"【用户{self.index}】【阅读状态】:一会儿再来看看{res}")
                    else:
                        await self.get_read_host()
                        
                elif res['result']['us']==2:
                    print(f"【用户{self.index}】【账号状态】:不出意外应该是黑号了")
                    return;
                else:
                    print(f"【用户{self.index}】【账号状态】:未知状态")                    
            else:
                print(f"【用户{self.index}】【错误】:获取用户信息失败 {res}")
        else:
            print("请求出现了问题，稍后再来看吧")
    
    
    async def process_account(self,index, ck,  sleep_time=None):
        self.index = index
        if sleep_time:
            print(f"【用户{self.index}】:随机休息{sleep_time}秒，我怕你点不了那么多")
            await asyncio.sleep(sleep_time)
        print(f"【用户{self.index}】【开始】:{'='*10}执行任务{'='*10}")
        
        cookie=ck.split("&")
        self.un=cookie[0]
        self.token=cookie[1]
        
        await self.user_info()
        await self.do_read_task()
        await self.close()
        print(f"【用户{self.index}】【结束】:{'='*10}结束执行{'='*10}")

async def check_env():
    
    cks = os.getenv('hhydcks')
    if cks is None:
        print("花花ck为空,请去抓包'un和token' 多账户请用@分割")
        exit()
    
    return cks.split("@") , wxpuser_uid.split('@'), topicid, wxpuser_token

async def main():
    cks_list = await check_env()
    use_concurrency = os.environ.get('multi_hhyd', 'false').lower() == 'true'
    from random import choice
    if use_concurrency:
        tasks = []
        random_sleep_list = [i * random.randint(50, 65) for i in range(len(cks_list))]
        for index, ck in enumerate(cks_list):
            abc = Hhyd()
            tasks.append(abc.process_account(index+1, ck,  sleep_time=random_sleep_list[index]))
        await asyncio.gather(*tasks)
    else:
        for index, ck in enumerate(cks_list):
            abc = Hhyd()
            await abc.process_account(index+1, ck)
  

if __name__ == '__main__':
    asyncio.run(main())