#!/usr/bin/env python
# -*- coding:utf-8
"""
@FileName :main.py
@Time :2024/5/914:17
@Author :Hhx06
@Desc :
"""
import pymysql

from phoneRankDataParse import mysqlConfig


def main():
    mysqlData = mysqlConfig.get_mysql_config()
    if len(mysqlData) < 3:
        return
    # MySQL 连接信息
    host = mysqlData[0]
    user = mysqlData[1]
    password = mysqlData[2]
    database = 'phone'

    # 连接到 MySQL 数据库
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()

    # 执行 SELECT 查询
    select_query = "SELECT rank,name FROM mobile_phones"
    cursor.execute(select_query)

    # 获取查询结果
    results = cursor.fetchall()
    for row in results:
        rank, name = row
        # 查找namecpu
        select_query1 = "SELECT id FROM cs_android WHERE cpu LIKE %s "
        cursor.execute(select_query1, ('%' + name + '%',))
        results1 = cursor.fetchall()
        if len(results1) > 0:
            for rr in results1:
                update_query = "UPDATE cs_android SET rank = %s WHERE id = %s"
                cursor.execute(update_query, (rank, rr))
        else:
            # 查找namecpu
            select_query1 = "SELECT id FROM cs_ios WHERE cpu LIKE %s "
            cursor.execute(select_query1, ('%' + name + '%',))
            results1 = cursor.fetchall()
            if len(results1) > 0:
                for rr in results1:
                    update_query = "UPDATE cs_ios SET rank = %s WHERE id = %s"
                    cursor.execute(update_query, (rank, rr))

    # 提交事务
    conn.commit()

    # 关闭游标和连接
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
