import time
import requests
import sys
import getopt
import os

"""
    作用
    推送ipv6地址到虾推啥小程序,充当辣鸡ddns

    参数说明
    token   :微信虾推啥的token
    from    :消息来源
    
        by kiekio
"""

ip_check_time_s = 60 * 10



taken = ""
data_source  = ""

if (len(sys.argv) < 2):
    print("miaomiaomiao")
    sys.exit(1)

try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["token=", "from="])
except getopt.GetoptError:
    print("喵喵喵")
    sys.exit(2)

for opt, arg in opts:
    if (opt == "--token"):
        taken = arg
    elif (opt == "--from"):
        data_source = arg

def ip_is_valid(ip_addr):
    ping_ok = False
    result = os.popen("ping " + ip_addr + " -n 1")
    text = result.read()
    if ("0%" in text):
        ping_ok = True
    else:
        pass

    return ping_ok

def getIpv6Addr() -> list:
    """
    返回ipv6地址list
    原理:通过解析ipconfig命令,获取"find_test = "临时 IPv6 地址. . . . . . . . . . : "后续的字符
         该地址可能有多个
    """
    cmd_text = os.popen("ipconfig").read()
    res = []
    find_test = "临时 IPv6 地址. . . . . . . . . . : "

    position_begin = 0
    while (True):
        position_begin = cmd_text.find(find_test, position_begin)
        if (position_begin == -1):
            break
        else:
            position_begin = position_begin + len(find_test)
            position_return = cmd_text.find("\n", position_begin)
            ipv6_str_len = position_return - position_begin

            res.append(cmd_text[position_begin : position_begin + ipv6_str_len])

            position_begin = position_begin + ipv6_str_len

    return res

def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def generateData(time, ipv6 : list, data_source = ""):
    despStr = ""
    despStr = despStr + time + "\n"
    for ipv6_i in ipv6:
        despStr = despStr + ipv6_i + "\n"

    textStr = "ipv6地址更新"
    textStr = textStr + "-" + data_source
    data = {
        "text" : textStr,
        "desp" : despStr
    }
    return data

def networkConnect():
    return ip_is_valid("www.bing.com")

def sendWxMessage(time, ipv6 : list, taken, data_source = ""):
    '''
    res:网络连接正常时返回True 否则返回Flase
    '''
    res = False
    if (networkConnect() == True):
        httpStr = "http://wx.xtuis.cn/" + taken + ".send"
        post_res = requests.post(httpStr, data=generateData(time, ipv6, data_source))
        res = True
        print(post_res.reason)
    else:
        print("no network")
    return res

def ipv6_is_change(ipv6Addr_new : list, ipv6Addr_old : list):
    res = False
    new_len = len(ipv6Addr_new)
    old_len = len(ipv6Addr_old)

    if (new_len != old_len):
        res = True
    else:
        for new_i in ipv6Addr_new:
            if (new_i in ipv6Addr_old):
                pass
            else :
                res = True
                break

    return res

ipv6Addr_new_list = getIpv6Addr()
ipv6Addr_old_list = ipv6Addr_new_list
ipv6Addr_massge_is_send = False

# 开始运行
print("开始运行")

# 开始运行时无论如何都要发送一条消息
ipv6Addr_massge_is_send = sendWxMessage(getTime(), ipv6Addr_new_list, taken, data_source)

while(True):
    time.sleep(ip_check_time_s)

    ipv6Addr_new_list = getIpv6Addr()
    if (len(ipv6Addr_new_list) != 0 ):
        if (    (ipv6Addr_massge_is_send == False)  \
            or  (ipv6_is_change(ipv6Addr_new_list, ipv6Addr_old_list)) ):
            ipv6Addr_old_list = ipv6Addr_new_list
            ipv6Addr_massge_is_send = sendWxMessage(getTime(), ipv6Addr_new_list, taken, data_source)




