# -*- coding: UTF-8 -*-
import pymysql
from verify_ip import verify
import time

def connect_to_sql():
    db = pymysql.connect(host="123.206.226.163", port=3306, user="root", password="root", database="pool_of_ip")
    cursor = db.cursor()
    return db,cursor

if __name__ == '__main__':

    while True:
        conn, cursor = connect_to_sql()
        try:
            cursor.execute('select * from pool_of_ip')
            results = cursor.fetchall()
            for ip_record in results:
                if verify(ip_record[0]):
                    print('%s 此ip可用' % ip_record[0])
                else:
                    print('%s ip不可用（将删除）' % ip_record[0])
                    cursor.execute('delete from pool_of_ip where ip_address = "%s"' % ip_record[0])
                    conn.commit()

        except:
            print('更新失败')
        finally:
            cursor.close()
            conn.close()
            time.sleep(10)