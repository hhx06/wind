#!/usr/bin/env python
# -*- coding:utf-8
"""
@FileName :main.py
@Time :2024/5/616:20
@Author :Hhx06
@Desc :
"""
import os
import shutil


def merge_files(folder_path, output_file):
    # 检查文件夹路径是否存在
    if not os.path.exists(folder_path):
        print("文件夹路径不存在！")
        return

    # 打开合并后的输出文件
    with open(output_file, 'wb') as out_file:
        # 遍历文件夹中的所有文件
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # 读取文件内容并写入到输出文件中
                with open(file_path, 'rb') as in_file:
                    shutil.copyfileobj(in_file, out_file)
                # 添加换行符
                out_file.write(b'\n')


def main():
    # 文件夹路径
    folder_path = "./proto_stat"
    # 合并后的输出文件路径
    output_file = "output.txt"

    # 调用合并函数
    merge_files(folder_path, output_file)

    print("文件合并完成！")


if __name__ == '__main__':
    main()
