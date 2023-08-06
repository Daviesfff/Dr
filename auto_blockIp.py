#!/usr/bin/env python3
import time
import os
import subprocess
import re
#打开安全日志
Logfile = '/var/log/secure'
#黑名单
hostDeny = '/etc/hosts.deny'
#封禁阈值
passwod_wrong_number = 5
#获取已经加入黑名单的IP，转换成字典


def getDenies():
    deniedDict ={}
    list = open(hostDeny).readlines()
    for ip in list:
        group =re.search(r'(\d+\.\d+\.\d+\.\d+)',ip)
        if group:
            deniedDict[group[1]] = '1'
    return deniedDict


#监控方法
def monitor(Logfile):
    #统计密码错误的次数
    tempIP = {}
    #调用这个方法,，保存已经拉黑的IP
    deniedDict = getDenies()
    #读取安全日志
    Popen = subprocess.Popen('tail -f '+Logfile,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell = True)\
    #开始监控
    while True:
        time.sleep(0.1)
        line = Popen.stdout.readline().strip()
        if line:
            group = re.search('Invaild user \w+ from (\d+\.\d+\.\d+\.\d+)',str(line))
            #不存在用户直接封
            if group and not deniedDict.get(group[1]):
                subprocess.getoutput('echo \'sshd:{}\' >> {}'.format(group[1],hostDeny))
                deniedDict[group[1]] = '1'
                time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                print('{}  add ip :{} to hosts.deny for invalid user'.format(time_str,group[1]))
                continue
            #用户名合法(有这个用户)，但是密码错误
            group = re.search('Failed password for \w+ from (\d+\.\d+\.\d+\.\d+)',str(line))
            if group:
                ip =group[1]
                #统计IP错误的次数
                if not tempIP.get(ip):
                    tempIP[ip] = 1
                else:
                    tempIP[ip] =tempIP[ip]+1
                #如果错误次数大于5的时候，直接封禁
                if tempIP[ip] > passwod_wrong_number and not deniedDict.get(ip):
                    del tempIP[ip]
                    subprocess.getoutput('echo \'sshd:{}\' >> {}'.format(ip,hostDeny))
                    deniedDict[ip] = '1'
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    print('{} --- add ip :{} to hosts.deny for invalid password'.format(time_str,ip))
if __name__ == '__main__':
    monitor(Logfile)