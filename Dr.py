#!/usr/bin/env python
#-*- coding :utf-8 -*-
#Author : Daveis

import requests
from sys import argv
from multiprocessing import Pool
def do_main_scan(domain_name,sub_domain_name):
    for sub in sub_domain_name:
        headers = {
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        }
        url = f'http://{sub}.{domain_name}'
        try:
            #requests.head(headers)
            requests.get(url)
            print(f'[*]{url}子域名存在')
        except requests.ConnectionError:
            #print('Error')
            pass
#创建进程池:
def multiprocess_Pool():
    p = Pool(4)
    for sub in sub_dom:
        p.apply_async(do_main_scan,args = (domain_name,sub))
        p.close()
        p.join()

if __name__ =='__main__':
    try:
        script,subdomain,domain_name= argv
    except:
        print("请按正确的格式进行输入：python 脚本名称 字典位置 域名")

    #读取字典：
    with open('subdomain.txt','r') as file:
        file_read = file.read()
        sub_dom = file_read.splitlines()
    #调用
    multiprocess_Pool()
