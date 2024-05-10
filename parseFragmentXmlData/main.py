#!/usr/bin/env python
# -*- coding:utf-8
"""
@FileName :main.py
@Time :2024/4/1217:58
@Author :Hhx06
@Desc :
"""

import xml.etree.ElementTree as ET


def main():
    # 定义 XML 数据
    xml_data = '''
   <data id="1" name="随机先锋碎片" quality="4" fragment_type="3" fragment_value="27" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="2" name="随机斗士碎片" quality="4" fragment_type="3" fragment_value="28" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="3" name="随机刺客碎片" quality="4" fragment_type="3" fragment_value="29" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="4" name="随机射手碎片" quality="4" fragment_type="3" fragment_value="30" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="5" name="随机神秘碎片" quality="4" fragment_type="3" fragment_value="31" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="6" name="随机法师碎片" quality="4" fragment_type="3" fragment_value="32" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="7" name="随机联邦碎片" quality="4" fragment_type="3" fragment_value="33" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="8" name="随机咆哮军团碎片" quality="4" fragment_type="3" fragment_value="34" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="9" name="随机暗域碎片" quality="4" fragment_type="3" fragment_value="35" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="10" name="随机伙伴碎片" quality="4" fragment_type="3" fragment_value="36" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="11" name="自选先锋碎片" quality="4" fragment_type="3" fragment_value="37" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="12" name="自选斗士碎片" quality="4" fragment_type="3" fragment_value="38" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="13" name="自选刺客碎片" quality="4" fragment_type="3" fragment_value="39" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="14" name="自选射手碎片" quality="4" fragment_type="3" fragment_value="40" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="15" name="自选神秘碎片" quality="4" fragment_type="3" fragment_value="41" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="16" name="自选法师碎片" quality="4" fragment_type="3" fragment_value="42" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="17" name="自选联邦碎片" quality="4" fragment_type="3" fragment_value="43" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="18" name="自选咆哮军团碎片" quality="4" fragment_type="3" fragment_value="44" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="19" name="自选暗域碎片" quality="4" fragment_type="3" fragment_value="45" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="20" name="自选伙伴碎片" quality="4" fragment_type="3" fragment_value="46" combine_num="100" gm="1" max_num="0" remind_size="1000" warn_size="1000000" />
    <data id="100000" name="龙血宝珠碎片" quality="6" fragment_type="10" fragment_value="100000" combine_num="30" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="100100" name="奈落的圣杯碎片" quality="6" fragment_type="10" fragment_value="100100" combine_num="30" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="100200" name="灵魂釜锅碎片" quality="5" fragment_type="10" fragment_value="100200" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="100300" name="梦境水晶碎片" quality="5" fragment_type="10" fragment_value="100300" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="100400" name="血精石护符碎片" quality="5" fragment_type="10" fragment_value="100400" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="100500" name="再生药剂碎片" quality="4" fragment_type="10" fragment_value="100500" combine_num="20" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="100600" name="以太沙漏碎片" quality="4" fragment_type="10" fragment_value="100600" combine_num="20" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="110000" name="怒风战刃碎片" quality="6" fragment_type="10" fragment_value="110000" combine_num="30" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="110100" name="红龙之卵碎片" quality="6" fragment_type="10" fragment_value="110100" combine_num="30" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="110200" name="奈落的呼唤碎片" quality="5" fragment_type="10" fragment_value="110200" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="110300" name="占梦师的神灯碎片" quality="5" fragment_type="10" fragment_value="110300" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="110400" name="奈落的视界碎片" quality="5" fragment_type="10" fragment_value="110400" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="110500" name="错乱之书碎片" quality="4" fragment_type="10" fragment_value="110500" combine_num="20" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="110600" name="月蚀提灯碎片" quality="4" fragment_type="10" fragment_value="110600" combine_num="20" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="120000" name="湮灭手套碎片" quality="6" fragment_type="10" fragment_value="120000" combine_num="30" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="120100" name="黄金圣甲虫碎片" quality="6" fragment_type="10" fragment_value="120100" combine_num="30" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="120200" name="旅法者的罗盘碎片" quality="5" fragment_type="10" fragment_value="120200" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="120300" name="界域观测者碎片" quality="5" fragment_type="10" fragment_value="120300" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="120400" name="夜之挽歌碎片" quality="5" fragment_type="10" fragment_value="120400" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="120500" name="振奋号角碎片" quality="4" fragment_type="10" fragment_value="120500" combine_num="20" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="120600" name="神器锻造者碎片" quality="4" fragment_type="10" fragment_value="120600" combine_num="20" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="130000" name="反相秒表碎片" quality="6" fragment_type="10" fragment_value="130000" combine_num="30" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="130100" name="女妖魔镜碎片" quality="6" fragment_type="10" fragment_value="130100" combine_num="30" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="130200" name="绿蜜酒碎片" quality="5" fragment_type="10" fragment_value="130200" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="130300" name="星界定位仪碎片" quality="5" fragment_type="10" fragment_value="130300" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="130400" name="星界之钥碎片" quality="5" fragment_type="10" fragment_value="130400" combine_num="25" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="130500" name="夜语蜡烛碎片" quality="4" fragment_type="10" fragment_value="130500" combine_num="20" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    <data id="130600" name="魔法卷轴碎片" quality="4" fragment_type="10" fragment_value="130600" combine_num="20" gm="1" max_num="0" remind_size="10000" warn_size="10000" />
    '''

    # 解析 XML 数据
    root = ET.fromstring('<root>' + xml_data + '</root>')

    # 获取所有<data>标签的id属性值
    ids = [data.get('id') for data in root.findall('data')]

    # 打印所有的id
    print(ids)


if __name__ == '__main__':
    main()
