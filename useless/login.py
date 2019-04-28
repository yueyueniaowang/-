#coding = utf-8

import requests
from bs4 import BeautifulSoup
import bs4
"""
try:
    import cookielib
    print("user cookielib in python2.")
except:
    import http.cookiejar as cookielib
    print(f"user cookielib in python3.")
"""


def rea_cookies(cookies):
    #this a def to create the real cookies which can be directly used in the requests
    rea_cookie = ""
    for key,value in cookies.items():
        rea_cookie = rea_cookie+key+"="+value+";"
    rea_cookie = rea_cookie + "selectionBar=12580302"
    print("cookie为",rea_cookie)
    return rea_cookie


#创建一个session,所有在s中的request都共享cookie
s = requests.session()
#添加cookie
s.cookies.set("selectionBar","12580302")


useragent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
headers0 = {
    'User-Agent': useragent,
}


def get_cookies():
    # this is a def to get the cookie,when we first go to the website

    print("********************************")
    print("准备cookie中")
    geturl = "http://zhjw.scu.edu.cn/login"
    try:
        r = s.get(geturl,headers = headers0)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("准备成功")
        print("cookie为" ,s.cookies.get_dict())
        #将cookie以字典的形式返回
        return r.cookies.get_dict()
    except:
        print(r.status_code)
        print("准备失败")
    finally:
        print("********************************")


def scu_login(j_username,j_password):
    #这里登录教务处网站，将cookie放到后台自己cookie身份验证的地方

    print("********************************")
    print("开始模拟登陆四川大学本科教务系统")
    postUrl = 'http://zhjw.scu.edu.cn/j_spring_security_check'
    postData = {
        "j_username":j_username,
        "j_password":j_password,
        "j_captcha1":"error",
    }
    #print(headers0)
    try:
        r = s.post(postUrl, data = postData, headers = headers0)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("登录成功")
        #print(s.cookies.get_dict())
        #print(r.text)
    except:
        print(r.status_code)
        print("登录失败")
    finally:
        print("********************************")


def scu_index():
    #this is a def to use cookie to get the index page.
    print("********************************")
    print("开始访问主页面")
    geturl = "http://zhjw.scu.edu.cn/index.jsp"
    try:
        r = s.get(geturl,timeout = 30, headers = headers0)
        r.raise_for_status()
        print(r.apparent_encoding)
        r.encoding = r.apparent_encoding
        #print(r.status_code)
        print("访问成功")
        #print(r.text)
    except:
        print(r.status_code)
        print("访问失败")
    finally:
        print("********************************")


def evaluate():
    #this is the def to compelete the "一键评教"，该进方法可以为从获得token的文档中，获得题型，从而不需要通过判断类型来得到题的类型
    print("********************************")
    print("开始爬取评价表单")
    posturl1 = "http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/search"
    postdata1 = {

    }

    try:
        global dict1
        r = s.post(posturl1,data = postdata1,headers = headers0)
        r.raise_for_status()
        #print(r.apparent_encoding)
        r.encoding = r.apparent_encoding
        #print(r.text)
        #print("**************************")
        dict1 = eval(r.text)
        #for data in dict1["data"]:
            #print(str(data))
        print("成功")

    except:
        print(r.status_code)
        print("失败")

    finally:
        print("****************")

    print("********************************")
    print("开始获得tokenvalue")
    teacher_data = dict1["data"]
    posturl2 = "http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluationPage"

    for teacher in teacher_data:
        if teacher["isEvaluated"] == "是":
            continue
        else:
            postdata2 = {
                "evaluatedPeople":teacher["evaluatedPeople"],
                "evaluatedPeopleNumber":teacher["id"]["evaluatedPeople"],
                "questionnaireCode":teacher["id"]["questionnaireCoding"],
                "questionnaireName":teacher["questionnaire"]["questionnaireName"],
                "evaluationContentNumber": teacher["id"]["evaluationContentNumber"],
                "evaluationContentContent":None,

            }
            r1 = s.post(posturl2,data = postdata2,headers = headers0)
            r1.raise_for_status()
            r1.encoding = r1.apparent_encoding
            data = r1.text
            soup = BeautifulSoup(data, 'html.parser')
            tokenvalue = soup.find('input',attrs={"name":"tokenValue"}).get('value')
            print("lalallalalallalallall",tokenvalue)
            if teacher["questionnaire"]['questionnaireName'] == '学生评教（课堂教学）':
                postdata3 ={
                        "tokenValue":tokenvalue,
                        "questionnaireCode": teacher["id"]["questionnaireCoding"],
                        "evaluationContentNumber": teacher["id"]["evaluationContentNumber"],
                        "evaluatedPeopleNumber": teacher["id"]["evaluatedPeople"],
                        "0000000036":"10_1",
                        "0000000037":"10_1",
                        "0000000038":"10_1",
                        "0000000039":"10_1",
                        "0000000040":"10_1",
                        "0000000041":"10_1",
                        "0000000042":"10_1",
                        "zgpj":"老师是好老师",
                }
                #print(postdata3)
                posturl3 = "http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluation"
                r2 =s.post(posturl3,data = postdata3,headers=headers0)
                r2.raise_for_status()
                r2.encoding = r2.apparent_encoding
                print(r2.text)
            elif teacher["questionnaire"]['questionnaireName'] == '学生评教（实践教学）':
                postdata3 = {
                    "tokenValue": tokenvalue,
                    "questionnaireCode": teacher["id"]["questionnaireCoding"],
                    "evaluationContentNumber": teacher["id"]["evaluationContentNumber"],
                    "evaluatedPeopleNumber": teacher["id"]["evaluatedPeople"],
                    "0000000089": "10_1",
                    "0000000090": "10_1",
                    "0000000091": "10_1",
                    "0000000092": "10_1",
                    "0000000093": "10_1",
                    "0000000094": "10_1",
                    "0000000095": "10_1",
                    "zgpj": "老师是好老师",
                }
                posturl3 = "http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluation"
                r2 = s.post(posturl3, data=postdata3, headers=headers0)
                r2.raise_for_status()
                r2.encoding = r2.apparent_encoding
                print(r2.text)
            elif teacher["questionnaire"]['questionnaireName'] == '研究生助教评价':
                postdata3 = {
                    "tokenValue": tokenvalue,
                    "questionnaireCode": teacher["id"]["questionnaireCoding"],
                    "evaluationContentNumber": teacher["id"]["evaluationContentNumber"],
                    "evaluatedPeopleNumber": teacher["id"]["evaluatedPeople"],
                    "0000000028": "10_1",
                    "0000000029": "10_1",
                    "0000000030": "10_1",
                    "0000000031": "10_1",
                    "0000000032": "10_1",
                    "0000000033": "10_1",
                    "zgpj": "老师是好老师",
                }
                posturl3 = "http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluation"
                r2 = s.post(posturl3, data=postdata3, headers=headers0)
                r2.raise_for_status()
                r2.encoding = r2.apparent_encoding
                print(r2.text)
            else:
                print("完成")


def run():
    #主函数
    get_cookies()
    scu_login("2016141413013","19981026sun")
    #scu_index()
    evaluate()



run()


