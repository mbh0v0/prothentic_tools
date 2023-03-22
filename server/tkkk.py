import tkinter as tk
from tkinter import messagebox
from server.xshell import *


class Menu:
    @classmethod
    def menu(cls):
        menubar = tk.Menu(window)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='查询', menu=filemenu)
        window.config(menu=menubar)


class Logs:
    def __init__(self, tk):
        self.start = None
        self.btn_query = None
        self.tk = tk
        self.host_label = self.tk.Label(window, text='请输入主机：', font=('Arial', 14))
        self.host_input = self.tk.Entry(window, font=('Arial', 14))
        self.port_label = self.tk.Label(window, text='请输入端口：', font=('Arial', 14))
        self.port_input = self.tk.Entry(window, font=('Arial', 14))
        self.username_label = self.tk.Label(window, text='请输入用户名称：', font=('Arial', 14))
        self.username_input = self.tk.Entry(window, font=('Arial', 14))
        self.password_label = self.tk.Label(window, text='请输入密码：', font=('Arial', 14))
        self.password_input = self.tk.Entry(window, font=('Arial', 14))
        self.request_id_label = self.tk.Label(window, text='请输入request_id：', font=('Arial', 14))
        self.request_id_input = self.tk.Entry(window, font=('Arial', 14))
        self.start_time_label = self.tk.Label(window, text='请输入开始时间：', font=('Arial', 14))
        self.start_time_input = self.tk.Entry(window, font=('Arial', 14))
        self.end_time_label = self.tk.Label(window, text='请输入结束时间：', font=('Arial', 14))
        self.end_time_input = self.tk.Entry(window, font=('Arial', 14))

    def line_break(self, text):
        self.start = 1.3
        while True:
            pos = text.search("{2023", self.start, stopindex="end")
            if not pos:
                break
            text.insert(pos, '\n')
            self.start = pos + "+3c"

    def query_show(self):
        self.host_label.place(x=10, y=10)
        self.host_input.place(x=190, y=10)
        self.port_label.place(x=10, y=50)
        self.port_input.place(x=190, y=50)
        self.username_label.place(x=10, y=90)
        self.username_input.place(x=190, y=90)
        self.password_label.place(x=10, y=130)
        self.password_input.place(x=190, y=130)
        self.request_id_label.place(x=10, y=170)
        self.request_id_input.place(x=190, y=170)
        self.start_time_label.place(x=10, y=210)
        self.start_time_input.place(x=190, y=210)
        self.end_time_label.place(x=10, y=250)
        self.end_time_input.place(x=190, y=250)

    def login(self):
        try:
            host = self.host_input.get()
            port = self.port_input.get()
            name = self.username_input.get()
            password = self.password_input.get()
            request_id = self.request_id_input.get()
            ssss = SSH(host, port, name, password)
            log_info = ssss.find_log(request_id)
            text = tk.Text(window)
            text.place(x=10, y=310)
            text.insert("insert", log_info)
            self.line_break(text)
        except Exception as e:
            messagebox.showinfo("提示", "查询失败，原因：" + str(e))

    def query_error(self):
        try:
            start_time = self.start_time_input.get()
            end_time = self.end_time_input.get()
            host = self.host_input.get()
            port = self.port_input.get()
            name = self.username_input.get()
            password = self.password_input.get()
            ssss = SSH(host, port, name, password)
            error_info = ssss.find_error_log(start_time, end_time)
            error_info_label = tk.Label(window, text=error_info, font=('Arial', 14))
            error_info_label.place(x=10, y=390)
            text = tk.Text(window)
            text.place(x=10, y=310)
            text.insert("insert", error_info)
            self.line_break(text)
        except Exception as e:
            messagebox.showinfo("提示", "查询失败，原因：" + str(e))

    def query_btn(self):
        self.btn_query = tk.Button(window, text='根据request_id查询', command=self.login)
        self.btn_query.place(x=30, y=290)
        self.btn_query = tk.Button(window, text='根据时间段查询', command=self.query_error)
        self.btn_query.place(x=190, y=290)

    def log_show(self):
        pass

    def forget(self):
        pass


window = tk.Tk()
window.title('test')
window.geometry('1000x900')
Menu().menu()
log = Logs(tk)
log.query_show()
log.query_btn()
window.mainloop()
