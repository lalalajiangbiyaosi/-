# -*- coding: UTF-8 -*-

import requests
import re
# import pandas
import random
import xml
from bs4 import BeautifulSoup


def verify(ip):
    url = 'http://1212.ip138.com/ic.asp'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Referer':'http://www.ip138.com/',
        'Host':'1212.ip138.com',

    }

    proxies = {

        "http":ip
    }
    try:
        r = requests.get(url=url,headers=headers,proxies=proxies,verify=False,timeout=3)
        html = r.content.decode('gbk')
        # print(html)
        m = re.findall('\[(.*)\]', html)
        # print(m)
        if m[0] in ip :
            return True
        else:
            return False
    except:
        return False
    finally:
        pass
#
# if __name__ == '__main__' :
#     r = verify('121.43.227.212:808')
#     print(r)