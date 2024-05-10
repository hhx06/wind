#!/usr/bin/env python
# -*- coding:utf-8
"""
@FileName :main.py
@Time :2024/5/817:56
@Author :Hhx06
@Desc :
"""

import pymysql


def main():
    # 连接到 MySQL 数据库
    conn = pymysql.connect(
        host="10.18.40.214",
        user="root",
        password="root000",
        database="phone",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询，检查A表中的name是否可模糊匹配到B表中的cpu字段的值
    cursor.execute("""
        SELECT mobile_phones.name,mobile_phones.id
        FROM mobile_phones
        JOIN phone_info ON phone_info.cpu LIKE CONCAT('%', mobile_phones.name, '%')
    """)

    # 获取查询结果
    matching_names = cursor.fetchall()
    x = []
    # 打印匹配到的名称
    for row in matching_names:
        # print(row['name'], row['id'])
        if row['id'] not in x:
            x.append(row['id'])

    # 关闭游标和连接
    cursor.close()
    conn.close()
    # x.sort()
    # print(x)
    for i in range(1, 164):
        if i not in x:
            print(i)


if __name__ == '__main__':
    main()
