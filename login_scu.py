# coding；utf-8

"""
this is the module to
"""


import requests
from bs4 import BeautifulSoup
import re
from config import *
from random import choice
from captcha import captcha


class TakeLessions():
    def __init__(self):
        self.s = requests.session()
        self.headers = {
            "User-Agent": choice(user_agent_list)
        }
        
    def scu_get_cookies(self):
        # this is a function to get the cookie,when we first come to the Scu system
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
            # print("准备失败",r.status_code)
            pass
        finally:
            print("********************************")

    def scu_login(self,j_username, j_password):
        """
        这里登录教务处网站，使之前得到的session和自己的身份联系在一起，从而使得session的身份验证生效
        """
        captcha_class=captcha(self.s)
        j_captcha = captcha_class()
        print("********************************")
        print("开始模拟登陆四川大学本科教务系统")
        postUrl = 'http://zhjw.scu.edu.cn/j_spring_security_check'
        postData = {
            "j_username": j_username,
            "j_password": j_password,
            "j_captcha": j_captcha,
        }
        print("用户名为：",j_username)
        print("密码为：",j_password)
        print("验证码为：", j_captcha)
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
        # 若无，返回空列表
        result = pattern.findall(str(text))
        if result != None and result != []:
            return True
        else:
            return False


    def scu_get_search(self,kch,kxh):
        """
        获取想要查询的课程信息
        :param kch:
        :param kxh:
        :return:
        """
        # 类里面可以通用session.cookie
        # print(self.s.cookies.get_dict())
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
        # print(courses1)
        # 当已经选过或不存在的课，教务处不会返回
        if courses1 == []:
            print("该课已经选过或不存在")
            return False
        # courses2 = eval(r.text)
        # for key,value in courses2.items():
            # print(key,value)
        # for course in courses1:
            # print(course)
        return courses1

    def scu_get_ks(self,kch,kxh):
        postData = {}
        courses = self.scu_get_search(kch, kxh)
        # 解决课不存在或选过的问题
        if(courses == False):
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

    def scu_get_token_fajhh(self):
        """
        获得tokenvalue
        :return:
        """

        getUrl = "http://zhjw.scu.edu.cn/student/courseSelect/courseSelect/index"
        r = self.s.get(getUrl,headers = self.headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text,"html.parser")
        tokenValue = soup.find('input', attrs={"id": "tokenValue"}).get('value')
        fajhh = re.findall(r"/intentCourse/index\?fajhh=(\d+)'",r.text)[0]
        print("fajhh为",fajhh)
        print("获得token,fajhh")
        return tokenValue,fajhh

    


    def scu_post_cour(self,kch,kxh):
        """
        向服务器post课程
        """
        # 3种返回
        # 1. 课不存在或选过 2. 选课成功 3. 选课不符合要求 4. 没选中或者没有课余量等等，总之没得都成功的返回，就一直轮询
        print("*********************")
        print("开始抢课")
        postUrl = "http://zhjw.scu.edu.cn/student/courseSelect/selectCourse/checkInputCodeAndSubmit"
        tokenValue,fajhh = self.scu_get_token_fajhh()
        postData = {
            "dealType":"2",
            "tokenValue":tokenValue,
            "fajhh":fajhh
        }
        print(postData)
        
        result = self.scu_get_ks(kch=kch, kxh=kxh)
        # 解决课不存在或选过的问题
        if result == False:
            return False
        postData.update(result)
        print(postData)
        while True:
            #postData["tokenValue"] = self.scu_get_token()
            
            r = self.s.post(postUrl,data = postData,headers = self.headers, timeout = 2)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            text = eval(r.text)
            if text["result"] == "ok":
                return 1
            
            
            


    def is_success(self,list1):
        """
        查看提交成功
        :param list1:
        :return:
        """
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
        # print(r.text)
        # 使用try是防止选课选满返回的未知情况，因为没有教务处不可以对没有课余量的课程选
        try:
            # {"result":["311022030_01:对不起，课程和其他课程的上课时间冲突！"],"isFinish":true,"schoolId":"100006"},这是r.text的格式，其中如果用eval直接恢复，小写的true不可辨别（ameError: name 'true' is not defined），所以分割
            # 分割时候先分出来前半个字典，再将值给分出来
            result = r.text.split(",\"isF")[0].split("[")[1][:-1]
            print(result)
            # 判断三种情况
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
        self.scu_get_cookies()
        self.scu_login("2016141413013", "19981026sun")

if __name__ == "__main__":

    lessions = TakeLessions()
    lessions()

