#! /usr/bin/env python
#-*- coding:utf-8 -*-

import requests,wget,os
import urllib.request as req
from bs4 import BeautifulSoup as bs
# import query

# file_url = 'http://file.beval.xyz/IF.csv'
# print(file_url)
# filename = 'IF.csv'
# wget.download(file_url, filename)
# IF_file = open('IF.csv', 'r')
# IF_lines = IF_file.readlines()
# IF_file.close()
# print(IF_lines)
# # os.remove(filename)
# jname_col = []
# if_col = []
# for line in IF_lines:
#     # print(line)
#     jname_col.append(line.split(',')[0].upper())
#     if_col.append(line.split(',')[1].strip('\n'))

def main(jrnl):
    # global jname_col
    # global if_col
    # request body
    url = "https://api.scholarscope.cn/getsinglesearch.php"
    payload = 'jrnl='+req.pathname2url(jrnl)
    headers = {
        'authority': 'api.scholarscope.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 '
                    'Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://www.scholarscope.cn',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.scholarscope.cn/tools/singlesearch.html',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Extract IF
    IF_soup = bs(response.text, "html.parser")
    JInf = IF_soup.find_all("td")
    IF = []
    for i in JInf:
        i = i.text
        IF.append(i)
    if len(IF) > 1:
        return IF
    else:
        IF = [jrnl,'','not avaliable']
        return IF

    if jrnl in jname_col:
        IF = [jrnl,if_col[jname_col.index(jrnl)]]
        return IF
    else:
        return [jrnl,'Not avaliable']
    


    


def pmid(id):
    url = 'https://pubmed.ncbi.nlm.nih.gov/?term='+id
    response = requests.get(url,timeout=10)
    return response.url[-9:-1]
