# -*- coding: UTF-8 -*-
'''获取代理ip地址
Usage:
    getip <number>


'''
import sqlite3
import pandas as pd
import requests
from docopt import docopt
import pymysql
from multiprocessing import Pool,cpu_count
from verify_ip import verify
import time
def fetch_ip():

    proxies = {'http': '', 'https': ''}
    url = 'http://www.xicidaili.com/nn'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWNlMDIzOWE3YjZlM2E3YmRlMzk2Njc4MjgyNTIxNGIyBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWprcFo2M21mNWhOaUUzVHJoUEdHUUNjSXBUZnJnWG04azhSVW5jdEp2SVU9BjsARg%3D%3D--d4e915b90c94c04a2c7ddb53a40a6aba84f3ac48; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1499522800,1501127711; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1501127750',
        'Host': 'www.xicidaili.com',
        'If-None-Match': 'W/"0504c4298869ceb901a3ac3f11743fc1"',
        'Referer': 'http://www.xicidaili.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    }

    r = requests.get(url, headers=headers)
    html = r.content.decode('utf-8')
    dfs = pd.read_html(html)
    ips = dfs[0]
    ips = ips.ix[1:, [1, 2, 3, 4, 5, 8, 9]]

    ips.ix[:, 1] = ips.ix[:, 1] + ':' + ips.ix[:, 2]
    del ips[2]
    http = ips.ix[ips[5] == 'HTTP',[1,5]]
    https = ips.ix[ips[5] == 'HTTPS',[1,5]]
    # print('-----------------')
    ver = []
    # print(http.head(10))
    http1 = list(http[1])
    # print(http1)
    return http,http1

# for index,row  in http.iterrows():
#     try:
#         verify_result = verify(row[1])
#     except:
#         verify_result = False
#         continue
#     finally:
#         ver.append(verify_result)
#     print(ver)
# print(http.ix[ver,:])
def contect_db():
    conn = sqlite3.connect('pool_ip.db')
    cursor = conn.cursor()
    try:
        print('----尝试创建数据库表格----')
        cursor.execute('create table pool_of_ip (ip_address varchar(50) PRIMARY KEY )')
    except:
        print('----创建失败，表格已存在----')
    finally:
        pass
    return conn,cursor
def connect_to_centos():
    db = pymysql.connect(host="123.206.226.163", port=3306, user="root", password="root", database="pool_of_ip")
    cursor = db.cursor()
    return db,cursor
if __name__ == '__main__':
    arguments = docopt(__doc__)
    # print(arguments)
    num = int(arguments.get('<number>'))
    while True:
        conn,cursor = connect_to_centos()
        # conn = sqlite3.connect('pool_ip.db')
        # cursor = conn.cursor()
        # try:
        #     print('----尝试创建数据库表格----')
        #     cursor.execute('create table pool_of_ip (ip_address varchar(50) PRIMARY KEY )')
        # except:
        #     print('----创建失败，表格已存在----')
        # finally:
        #     pass
        http,http1 = fetch_ip()
        # print(ips.ix[0:num, [1, 5]])
        p = Pool(cpu_count())
        print('--------开始验证ip(http)代理---------')
        verify_result = p.map(verify,http1)

        for ip_record in list(http.ix[verify_result,1]):
            print(ip_record)
            try:
                cursor.execute('insert into pool_of_ip (ip_address) values ("%s")' % ip_record)
                print('----输出到数据库----')
            except:
                pass
            finally:
                pass
        cursor.close()
        conn.commit()
        conn.close()
        time.sleep(10)
