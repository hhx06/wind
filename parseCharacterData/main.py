#!/usr/bin/env python
# -*- coding:utf-8
"""
@FileName :main.py
@Time :2024/4/1218:04
@Author :Hhx06
@Desc :
"""
import openpyxl


def main():
    # 打开 Excel 文件
    wb = openpyxl.load_workbook('./character_companion_send_info.xlsx')

    # 选择第一个工作表
    sheet = wb.active

    # 获取第一列的值
    column_values = [cell.value for cell in sheet['A']]

    # 输出第一列的值
    print(column_values)


if __name__ == '__main__':
    main()
