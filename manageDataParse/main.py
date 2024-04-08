#!/usr/bin/env python
# -*- coding:utf-8
"""
@FileName :main.py
@Time :2024/4/817:24
@Author :Hhx06
@Desc : 打点数据解析
"""
import csv
import re


# 字符串是否含有某字符
def contains_char(s, char):
    return char in s


def contains_char_not(s, char):
    return char not in s


# 打开CSV文件
def readCsv(filePath):
    with open(filePath, 'r', encoding='utf-8') as csvfile:
        reader = filePath.reader(csvfile)
        # 遍历每一行数据
        for row in reader:
            # 处理每一行数据
            print(row)
            print("==============")


def readTxt(filePath, myMap, myTps):
    x = False
    with open(filePath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            # print(line.strip())
            if contains_char(line.strip(), "CostTime") and contains_char_not(line.strip(), "总体最热"):
                x = False
            if contains_char(line.strip(), "总体最热"):
                x = True
                result = line.strip().split(" ")
                if len(result) > 0:
                    k = 0
                    for v in result:
                        k += 1
                        if contains_char(v, "userCount"):
                            break
                    if k > 0 and len(result) > k + 1:
                        userCount = result[k]
                    # print("userCount:", userCount)
            if x:
                if contains_char(line.strip(), "hot"):
                    if userCount == 0:
                        continue
                    # 多个空格合为一个空格
                    result = re.sub(r'\s+', " ", line.strip()).split(" ")
                    # print("before")
                    for v in range(0, len(result)):
                        if result[v] == "hot" and len(result) > v + 5 and contains_char(result[v + 1], "ms"):
                            respTimeAll = result[v + 1][:-2]
                            messageCount = result[v + 4]
                            messageName = result[v + 5]
                            avgTime = float(respTimeAll) / float(messageCount)
                            if messageName not in myMap:
                                myMap[messageName] = [avgTime]
                            else:
                                myMap[messageName].append(avgTime)
                            maxTps = float(messageCount) / float(userCount) / float(60)
                            if myTps.get(messageName, {"tps": float('-inf')})["tps"] < maxTps:
                                myTps[messageName] = {"messageName": messageName, "tps": maxTps}
    return myMap, myTps


def getSortData(myMap, myTps, t):
    sum100 = 0
    for k, v in myMap.items():
        if len(v) >= 10:
            # 不会产生新的dist
            v.sort()
            v = v[:int(len(v) * 9 / 10)]
        myTps[k]["respTime"] = sum(v) / len(v)
        myTps[k]["costTps"] = sum(v) / len(v) * myTps[k]["tps"]
        t[k] = myTps[k]
        sum100 += myTps[k]["costTps"]
    return sorted(t.items(), key=lambda x: x[1]['costTps']), sum100


def main():
    myMap = {}
    myTps = {}
    t = {}
    myMap, myTps = readTxt("./proto_stat.log", myMap, myTps)
    tt, sum100 = getSortData(myMap, myTps, t)
    writeCsv("./x.csv", tt, sum100)


def writeCsv(new_csv, tt, sum100):
    sum90 = 0
    with open(new_csv, 'w+', newline='', encoding='gb18030') as csvfile:
        spamWriter = csv.writer(csvfile, dialect="excel")  # dialect可用delimiter= ','代替，后面的值是自己想要的符号
        # 如：spamWriter = csv.writer(csvfile,delimiter= '：')#dialect可用delimiter= ','
        spamWriter.writerow(
            ["协议", "最大人均tps", "单协议平均耗时", "单协议耗时*人均最大TPS", "是否压测"])
        for k, val in tt:
            sum90 += val["costTps"]
            line_data = []
            print(val)
            for k1, v1 in val.items():
                print(v1)
                line_data.append(v1)
            if sum90 > sum100 * 0.95:
                line_data.append("否")
            else:
                line_data.append("是")
            spamWriter.writerow(line_data)


if __name__ == '__main__':
    main()
