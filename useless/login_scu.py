# coding；utf-8

"""
this is the module to
"""



import base64
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import re
from config import *
from captcha import captcha
from random import choice

class Take_lessions():
    def __init__(self):
        self.s = requests.session()
        self.headers = {
            "User-Agent": choice(user_agent_list)
        }
        
    def scu_get_cookies(self):
        # this is a function to get the cookie,when we first come to the Scu system'
        print("********************************")
        print("准备cookie中")
        geturl = "http://zhjw.scu.edu.cn/login"
        try:
            r = self.s.get(geturl, headers=self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print("cookie为", self.s.cookies.get_dict())
            print("准备成功")
            # 将cookie以字典的形式返回
            return r.cookies.get_dict()
        except:
            #print("准备失败",r.status_code)
            pass
        finally:
            print("********************************")

    def get_captcha_pic(self):
        print("********************************")
        get_url = "http://zhjw.scu.edu.cn/img/captcha.jpg"
        try:
            r = self.s.get(get_url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print("获取验证码成功")
            image = Image.open(BytesIO(r.content))
            image.show()
            return r.content
    
        except:
            print("获取验证码失败", r.status_code)
        finally:
            print("********************************")

    def get_usekey_damagou(self):
        print("********************************")
        get_url = "http://www.damagou.top/apiv1/login.html?username=futai&password=111111"
        try:
            r = requests.get(get_url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print("获取dmagou平台userKey成功")
            return r.text
        except:
            print("获取dmagou平台userKey失败", r.status_code)
        finally:
            print("********************************")

    def get_english_captcha(self):
        captcha=self.get_captcha_pic()
        userkey = self.get_usekey_damagou()
        base64_data = base64.b64encode(captcha)
        print("********************************")
        postUrl = 'http://www.damagou.top/apiv1/recognize.html'
        postData = {
            "image": base64_data,
            "userkey": userkey,
            "type": "1003",
        }
        try:
            r = requests.post(postUrl, data=postData)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print(r.text)
            return r.text
        except:
            pass

    def scu_login(self,j_username, j_password):

        '''这里登录教务处网站，使之前得到的session和自己的身份联系在一起，从而使得session的身份验证生效'''
        print("********************************")
        print("开始模拟登陆四川大学本科教务系统")
        postUrl = 'http://zhjw.scu.edu.cn/j_spring_security_check'
        postData = {
            "j_username": j_username,
            "j_password": j_password,
            "j_captcha": self.get_english_captcha(),
        }
        print(j_username)
        print(j_password)
        
        try:
            r = self.s.post(postUrl, data=postData, headers=self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            if self.is_login(r.text):
                print("登录成功")
            else:
                print("用户名和密码错误")
            return self.is_login(r.text)
            # print(s.cookies.get_dict())
            # print(r.text)
        except:
            print(r.text)
            print("登录失败",r.status_code)
            return False
        finally:
            print("********************************")


    def is_login(self,text):
        pattern = re.compile(r"综合教务系统首页")
        #若无，返回空列表
        result = pattern.findall(str(text))
        if result != None and result != []:
            return True
        else:
            return False


    def scu_get_search(self,kch,kxh):
        "获取想要查询的课程信息"
        #类里面可以通用session.cookie
        #print(self.s.cookies.get_dict())
        postUrl = "http://zhjw.scu.edu.cn/student/courseSelect/freeCourse/courseList"
        postData = {
            "searchtj":kch,
            "xq":"0",
            "jc":"0",
            "kyl":"1",
            "kclbdm": None
        }

        r = self.s.post(postUrl, data= postData,headers =self.headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        courses1 = eval(eval(r.text)["rwRxkZlList"])
        #print(courses1)
        #当已经选过或不存在的课，教务处不会返回
        if courses1 == []:
            print("该课已经选过或不存在")
            return False
        #courses2 = eval(r.text)
        #for key,value in courses2.items():
            #print(key,value)
        #for course in courses1:
            #print(course)
        return courses1


    def scu_get_ks(self,kch,kxh):
        postData = {}
        courses = self.scu_get_search(kch, kxh)
        #解决课不存在或选过的问题
        if(courses ==False):
            return False
        for course in courses:
            if course["kxh"] == str(kxh) and course["kch"] == str(kch):
                print(course)
                postData["kcIds"] = course["kch"]+"_"+course["kxh"]+"_"+course["zxjxjhh"]
                postData["kcms"] = course["kcm"]
                return postData
            elif course == courses[-1]:
                print("参数不对")
                return False

    def scu_get_token(self):
        '''获得tokenvalue'''

        getUrl = "http://zhjw.scu.edu.cn/student/courseSelect/planCourse/index?fajhh=3334"
        r = self.s.get(getUrl,headers = self.headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text,"html.parser")
        tokenValue = soup.find('input', attrs={"name": "tokenValue"}).get('value')
        print("获得token")
        return tokenValue




    def scu_post_cour(self,kch,kxh,fajhh='3334'):
        '''向服务器post课程'''
        #3种返回
        #1. 课不存在或选过 2. 选课成功 3. 选课不符合要求 4. 没选中或者没有课余量等等，总之没得都成功的返回，就一直轮询
        print("*********************")
        print("开始抢课")
        postUrl = "http://zhjw.scu.edu.cn/student/courseSelect/freeCourse/waitingfor?dealType=5"
        postData = {
            "tokenValue":None,
            "fajhh":fajhh
        }
        result = self.scu_get_ks(kch=kch, kxh=kxh)
        #解决课不存在或选过的问题
        if result ==False:
            return False
        postData.update(result)
        while True:
            postData["tokenValue"] = self.scu_get_token()
            r = self.s.post(postUrl,data = postData,headers = self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            text = r.text
            pattern1 = re.compile(r"redisKey = \"\d+\"")
            pattern2 = re.compile(r"\d+")
            pattern3 = re.compile(r"kcNum = \"\d+\"")
            redisKey = pattern2.findall(pattern1.findall(text)[0])[0]
            kcNum =  pattern2.findall(pattern3.findall(text)[0])[0]
            result = self.is_success([kcNum,redisKey])
            #根据返回的三种情况向GUI做出合理的返回
            if result == None:
                continue
            elif result[0] == 1:
                return (True,result[1])
            elif result[0] ==2:
                return (False,result[1])


    def is_success(self,list1):
        '''查看提交成功'''
        kcNum = list1[0]
        redisKey = list1[1]
        postUrl = "http://zhjw.scu.edu.cn/student/courseSelect/selectResult/query"
        postData = {
            "kcNum":kcNum,
            "redisKey":redisKey
        }
        r = self.s.post(postUrl, data=postData, headers=self.headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        #print(r.text)
        #使用try是防止选课选满返回的未知情况，因为没有教务处不可以对没有课余量的课程选
        try:
            # {"result":["311022030_01:对不起，课程和其他课程的上课时间冲突！"],"isFinish":true,"schoolId":"100006"},这是r.text的格式，其中如果用eval直接恢复，小写的true不可辨别（ameError: name 'true' is not defined），所以分割
            # 分割时候先分出来前半个字典，再将值给分出来
            result = r.text.split(",\"isF")[0].split("[")[1][:-1]
            print(result)
            #判断三种情况
        except:
            return None
        else:
            if "选课成功" in result:
                return (1,result)
            elif "对不起" in result:
                return (2,result)
            else:
                return None


    def __call__(self):
        #print("call")
        #self.scu_get_cookies()
        self.scu_get_cookies()
        self.scu_login("2016141413013", "19981026sun")



    def run(self):
        self.scu_get_cookies()
        self.scu_login("2016141413013","19981026sun")
        #token = self.scu_get_token()
        #self.scu_post_cour()

if __name__ == "__main__":

    lessions = Take_lessions()
    lessions()
    #lessions.scu_post_cour("311143040","04")
