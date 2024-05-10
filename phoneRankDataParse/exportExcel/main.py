#!/usr/bin/env python
# -*- coding:utf-8
"""
@FileName :main.py
@Time :2024/5/1014:42
@Author :Hhx06
@Desc :
"""
import pymysql
import pandas as pd
from datetime import datetime

from phoneRankDataParse import mysqlConfig


def main():
    mysqlData = mysqlConfig.get_mysql_config()
    if len(mysqlData) < 3:
        return
    # 连接到 MySQL 数据库
    conn = pymysql.connect(
        host=mysqlData[0],
        user=mysqlData[1],
        password=mysqlData[2],
        database="phone",
        charset="utf8mb4"
    )

    # 从数据库中读取数据到DataFrame
    df = pd.read_sql("SELECT * FROM cs_android", conn)

    df1 = pd.read_sql("SELECT * FROM cs_ios", conn)

    # 关闭数据库连接
    conn.close()

    # 将DataFrame写入Excel文件
    df.to_excel("android" + datetime.now().strftime("%Y-%m-%d") + ".xlsx", index=False)
    df1.to_excel("ios" + datetime.now().strftime("%Y-%m-%d") + ".xlsx", index=False)

    print("导出成功！")


if __name__ == '__main__':
    main()
