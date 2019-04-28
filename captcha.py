# coding:utf-8


"""
this is the module to
Identificate verification code using the api of "http://www.damagou.top/"
"""

import base64
import requests
from PIL import Image
from io import BytesIO
from config import *
from random import choice

class captcha():
    def __init__(self,s,):
        if s is None:
            self.s = requests.session()
        else:
            self.s = s
        self.headers={
            "User-Agent": choice(user_agent_list)
        }
        
    def get_captcha_pic(self):
        print("********************************")
        get_url = "http://zhjw.scu.edu.cn/img/captcha.jpg"
        
        try:
            r = self.s.get(get_url,headers = self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print("获取验证码成功")
            # image = Image.open(BytesIO(r.content))
            # image.show()
            return r.content
    
        except:
            print("获取验证码失败", r.status_code)
        finally:
            print("********************************")
    
    def get_usekey_damagou(self,):
        print("********************************")
        get_url = "http://www.damagou.top/apiv1/login.html?username=futai&password=111111"
        try:
            r = requests.get(get_url,headers = self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print("获取dmagou平台userKey成功")
            return r.text
        except:
            print("获取dmagou平台userKey失败", r.status_code)
        finally:
            print("********************************")
    
    def get_english_captcha(self,captcha,userkey):
        base64_data = base64.b64encode(captcha)
        print("********************************")
        postUrl = 'http://www.damagou.top/apiv1/recognize.html'
        postData = {
            "image": base64_data,
            "userkey": userkey,
            "type": "1003",
        }
        try:
            r = requests.post(postUrl, data=postData,headers = self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print("破解验证码成功")
            return r.text
        except:
            print("破解验证码失败")
    
    def __call__(self):
        captcha = self.get_captcha_pic()
        userkey = self.get_usekey_damagou()
        return self.get_english_captcha(captcha,userkey)
        
def get_english_captcha(captcha,userkey):
    #base64_data = base64.b64encode(captcha)
    print("********************************")
    postUrl = 'http://www.damagou.top/apiv1/recognize.html'
    postData = {
        "image": base64_data,
        "userkey": userkey,
        "type": "1001",
    }
    try:
        r = requests.post(postUrl, data=postData)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("破解验证码成功")
        return r.text
        
    except:
        print("破解验证码失败")
        
        
def get_usekey_damagou():
    print("********************************")
    get_url = "http://www.damagou.top/apiv1/login.html?username=futai2&password=123456"
    try:
        r = requests.get(get_url)
        print(r.status_code)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("获取dmagou平台userKey成功")
        return r.text
    except:
        print("获取dmagou平台userKey失败")
    finally:
        print("********************************")
        
if __name__ == "__main__":
    import base64
    with open("./2.jpg", "rb") as f:
        # b64encode是编码，b64decode是解码
        base64_data = base64.b64encode(f.read())
        # base64.b64decode(base64data)
    userkey = get_usekey_damagou()
    print(get_english_captcha(base64_data,userkey))
