from paramiko import SSHClient, AutoAddPolicy
import datetime
from server.error import *


class SSH:
    def __init__(self, host, port, username, password):
        self.ssh = SSHClient()
        # 允许连接不在know_hosts文件里的主机
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        # 连接服务器
        self.ssh.connect(hostname=host, port=port, username=username, password=password)

    def command(self, command):
        # 执行命令
        stdin, stdout, stderr = self.ssh.exec_command(command)
        # 获取命令结果
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        # 将字节类型 转换为 字符串类型
        result = str(result, encoding='utf-8')
        return result

    def find_log(self, track_id):
        # 查询所有日志文件
        log_result = self.command("ls /home/public/logs/")
        result = log_result.split("\n")
        log_list = []
        for file in result:
            if file:
                if "log" in file:
                    log_list.append(file)
        # 遍历所有日志文件
        info_list = []
        for log_name in log_list:
            result = self.command("cat /home/public/logs/" + log_name + " | grep " + track_id + " | sort -r")
            result = result.split("\n")
            for log in result:
                if log:
                    # if "exit service" not in log and 'enter service' not in log and \
                    #         "finish http request" not in log and "start http request" not in log and\
                    #         "command not found" not in log:
                    if "command not found" not in log:
                        info = []
                        time = log[0:19]
                        if "[" in time:
                            time = log[1:20]
                        message = "unknown"
                        if "ERROR" in log:
                            message = "ERROR"
                        if "INFO" in log:
                            message = "INFO"
                        if "WARN" in log:
                            message = "WARN"
                        info.append(time)
                        info.append(get_server(log_name))
                        info.append(message)
                        info.append(log)
                        info_list.append(info)
        return info_list

    def find_error_log(self, start_time, end_time):
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        log_result = self.command("ls /home/public/logs/")
        result = log_result.split("\n")
        log_list = []
        for file in result:
            if file:
                if "log" in file:
                    log_list.append(file)
        # 遍历所有日志文件
        info_list = []
        for log_name in log_list:
            result = self.command("cat /home/public/logs/" + log_name + " | grep error | sort -r")
            result = result.split("\n")
            for log in result:
                if log:
                    # if "exit service" not in log and 'enter service' not in log and \
                    #         "finish http request" not in log and "start http request" not in log and\
                    #         "command not found" not in log:
                    if "command not found" not in log:
                        info = []
                        time = log[0:19]
                        if "[" in time:
                            time = log[1:20]
                        try:
                            log_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                            if start_time < log_time < end_time:
                                message = "unknown"
                                if "ERROR" in log:
                                    message = "ERROR"
                                if "INFO" in log:
                                    message = "INFO"
                                if "WARN" in log:
                                    message = "WARN"
                                info.append(time)
                                info.append(get_server(log_name))
                                info.append(message)
                                info.append(log)
                                info_list.append(info)
                        except Exception as e:
                            continue
        return info_list

    def close(self):
        # 关闭连接
        self.ssh.close()

