from server.xshell import SSH


def main():
    ssh = SSH("121.5.246.209", 22, "test", "CQiyV6NjNs4Memv6stw0PTwLjuKBql")
    # 查询所有日志文件
    log_result = ssh.command("ls /home/public/logs/")
    result = log_result.split("\n")
    log_list = []
    for i in result:
        if i:
            if "log" in i:
                log_list.append(i)
    # 遍历所有日志文件
    info_list = []
    for i in log_list:
        result = ssh.command("cat /home/public/logs/" + i + " |"
                         " grep 2d787db9-fc76-97f6-23e2-82466a373fa7 | sort -r")
        result = result.split("\n")
        for j in result:
            if j:
                if "exit service" not in j and 'enter service' not in j and\
                        "finish http request" not in j and "start http request" not in j:
                    info = []
                    time = i[0:22]
                    info.append(time)
                    info.append(i)
                    info.append(j)
                    info_list.append(info)
    print(info_list)

    # print(result[1])


if __name__ == '__main__':
    main()