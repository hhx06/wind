#!/usr/bin/env python
# -*- coding:utf-8
"""
@FileName :main.py
@Time :2024/5/618:41
@Author :Hhx06
@Desc :
"""


def main():
    data = {}

    # 数据
    data_str = """
    // 0.9.50-每日惊喜福利(102531-102540)
    MSG_C2S_DailySurpriseBenefit_ObtainRewards = 102531;   // 领取每日惊喜福利
    MSG_S2C_DailySurpriseBenefit_ObtainRewards = 102532;

    // 0.9.50-功能预览(102541-102550)
    MSG_C2S_FunctionPreview_ObtainRewards = 102541;   // 领取功能预览奖励
    MSG_S2C_FunctionPreview_ObtainRewards = 102542;
    """

    # 按行解析数据
    lines = data_str.strip().split("\n")
    for line in lines:
        # 分割每行数据
        parts = line.strip().split("=")
        if len(parts) != 2:
            continue
        key = parts[0].strip()
        value = parts[1].split(";")[1].strip()

        # 添加到数据字典中
        data[key] = value[3:]

    # 输出结果
    # for key, value in data.items():
        # print(f"data[\"{key}\"] = \"{value}\"")
    print(data)


if __name__ == '__main__':
    main()
