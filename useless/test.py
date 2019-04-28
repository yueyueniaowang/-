# -*- coding: utf-8 -*-

import requests
import re
from PIL import Image
import pytesseract
from PIL import Image
from PIL import Image,ImageTk
import tkinter as tk

# 简单插入显示
def show_jpg():
    root = tk.Tk()
    im=Image.open("index.jpg")
    img=ImageTk.PhotoImage(im)
    imLabel=tk.Label(root,image=img).pack()
    root.mainloop()




def test1():
    try:
        print("one")
    except:
        print("two")
    finally:
        print("three")

    print("four")



def test2():
    #空列表不等同于空
    a = []
    if a ==None:
        print(True)
    else:
        print(False)

def test3():
    text="The URL has moved <a href=\"http://zhjw.scu.edu.cn/index.jsp\">here</a>"
    pattern = re.compile(r"index.jsp")
    result = pattern.findall(text)
    if result != None and result != []:
        return True
    else:
        return False

import tesserocr
from PIL import Image

def test4():
    image = Image.open("captcha.jpg")
    result = tesserocr.image_to_text(image)
    print(result)

import requests
from bs4 import BeautifulSoup
import re

def test5():
    print("********************************")
    geturl = "http://www.damagou.top/apiv1/login.html?username=futai&password=111111"
    try:
        r = requests.get(geturl)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print(r.text)
        return r.text
    except:
        print("准备失败", r.status_code)
    finally:
        print("********************************")
 
import base64
def test6():
    with open("captcha.jpg", "rb") as f:
        image_data = f.read()
        print(image_data)
        base64_data = base64.b64encode(image_data)
    print("********************************")
    postUrl = 'http://www.damagou.top/apiv1/recognize.html'
    postData = {
        "image": base64_data,
        "userkey": test5(),
        "type": "1003",
    }
    try:
        r = requests.post(postUrl, data=postData)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print(r.text)
    except:
        pass


def test7():
    image = Image.open('captcha.jpg')
    print(image)
    image = image.convert('L')
    threshold = 127
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    
    image = image.point(table, '1')
    image.show()
    
    result = tesserocr.image_to_text(image)
    print(result)
test7()
    