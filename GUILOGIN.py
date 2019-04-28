from tkinter import messagebox
from GUIMainPage import *
from login_scu import TakeLessions


class Login(object):
    
    #  这是系统的登录界面
    def __init__(self,lessons = None,master =None):
        self.lessions = TakeLessions()
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("四川大学抢课软件1.0")
        self.root.geometry('500x313')
        # 运行代码时记得添加一个gif图片文件，不然是会出错的，只能是gif文件
        self.canvas = tkinter.Canvas(self.root, height=300, width=500)  # 创建画布，也就是图片在画面上的大小
        self.image_file = tkinter.PhotoImage(file='scu.jpg.gif')  # 加载图片文件
        self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.image_file)  # 将图片置于画布上
        self.canvas.pack(side='top')  # 放置画布（为上端）

        # 创建一个整型变量
        self.v = tkinter.IntVar()
        # 创建一个`label`名为`Account: `
        self.label_account = tkinter.Label(self.root, text='用户名:')
        # 创建一个`label`名为`Password: `
        self.label_password = tkinter.Label(self.root, text='密码:')

        # 创建一个账号输入框,并设置尺寸
        self.input_account = tkinter.Entry(self.root, width=30)
        # 创建一个密码输入框,并设置尺寸,密码不可见是*
        self.input_password = tkinter.Entry(self.root, show='*', width=30)

        # 创建一个登录系统的按钮
        self.login_button = tkinter.Button(self.root, command=self.backstage_interface, text="登录", width=10)
        self.pass_button=tkinter.Checkbutton(self.root,text="记住密码",padx=20,variable=self.v)

        #不可以在下面，检查时候记住密码，因为在初始化的时候，是没有东西的。容易报错
        #self.is_rem_pass()
        # 完成布局
        self.label_account.place(x=60, y=170)
        self.label_password.place(x=60, y=195)
        self.input_account.place(x=135, y=170)
        self.input_password.place(x=135, y=195)
        self.login_button.place(x=140, y=235)
        self.pass_button.place(x=240,y = 235)
        # 进行登录信息验证

    def backstage_interface(self):
        account = self.input_account.get()
        password = self.input_password.get()
        # 对账户信息进行验证，普通用户返回user，管理员返回master，账户错误返回noAccount，密码错误返回noPassword
        verifyResult = self.lessions.scu_login(account,password)
        if verifyResult == True:
            self.is_rem_pass()
            self.root.destroy()
            Mainpage(self.lessions)
        elif verifyResult == False:
            #不知道为什么在这里不起作用
            #self.is_rem_pass()
            tkinter.messagebox.showinfo(title='四川大学抢课软件1.0', message='账号/密码错误请重新输入!')


    def is_rem_pass(self):
        if self.v == 1:
            with open("pass1.txt","w") as f:
                f.seek(0)
                f.truncate()
                f.write(self.input_account.get())
                f.write(self.input_password.get())



