import pandas as pd
import streamlit as st
from server.xshell import *
from server.error import *


class Query:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.request_id = None
        self.password = None
        self.name = None
        self.port = None
        self.host = None
        self.date = None
        self.ssh = None
        self.log_info = None
        self.log_info2 = None

    def log_request_id(self, host, port, username, password, request_id):
        try:
            if self.ssh:
                log_info = self.ssh.find_log(request_id)
            else:
                self.ssh = SSH(host, port, username, password)
                log_info = self.ssh.find_log(request_id)
            return log_info
        except Exception as e:
            e = get_error(e)
            st.write("提示", "查询失败，原因：" + str(e))

    def log_time(self, host, port, username, password, start_time, end_time):
        try:
            if self.ssh:
                log_error_info = self.ssh.find_error_log(start_time, end_time)
            else:
                self.ssh = SSH(host, port, username, password)
                log_error_info = self.ssh.find_error_log(start_time, end_time)
            return log_error_info
        except Exception as e:
            e = get_error(e)
            st.write("提示", "查询失败，原因：" + str(e))

    def show_color(self, info):
        if 'ERROR' in str(info):
            color = 'red'
            return 'color:%s' % color
        elif 'WARN' in str(info):
            color = 'yellow'
            return 'color:%s' % color


def main_page():
    st.title('查询日志')
    host = st.text_input('请输入主机', '')
    port = st.text_input('请输入端口', '')
    username = st.text_input('请输入用户名', '')
    password = st.text_input('请输入密码', '', type='password')
    st.subheader('根据请求id查询日志')
    request_id = st.text_input('请求id')
    df = Query()
    request_log = get_request_log()
    if st.button('根据请求id查询日志'):
        log_info = df.log_request_id(host, port, username, password, request_id)
        set_request_log(log_info)
        request_log = get_request_log()
    if request_log:
        column1 = ['时间', '服务', '错误类型', '详情']
        request_log.append(column1)
        log_info2 = pd.DataFrame(request_log[0:-2], columns=request_log[-1])
        log_info2 = log_info2.style.applymap(df.show_color, subset=['错误类型'])
        st.dataframe(log_info2)
    else:
        pass
    st.subheader('根据时间段查询日志')
    d_start = st.date_input('开始日期', datetime.date(2023, 3, 14))
    t_start = st.time_input('开始时间', datetime.time())
    d_end = st.date_input('结束日期', datetime.date(2023, 3, 16))
    t_end = st.time_input('结束时间', datetime.time())
    start_time = str(d_start) + ' ' + str(t_start)
    end_time = str(d_end) + ' ' + str(t_end)
    time_log = get_time_log()
    if st.button('根据时间段查询日志'):
        time_log_info = df.log_time(host, port, username, password, start_time, end_time)
        set_time_log(time_log_info)
        time_log = get_time_log()
    if time_log:
        column1 = ['时间', '服务', '错误类型', '详情']
        time_log.append(column1)
        log_info2 = pd.DataFrame(time_log[0:-2], columns=time_log[-1])
        log_info2 = log_info2.style.applymap(df.show_color, subset=['错误类型'])
        st.dataframe(log_info2)
    else:
        pass


if __name__ == '__main__':
    main_page()

