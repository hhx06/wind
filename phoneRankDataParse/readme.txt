1、执行phoneD目录下文件获取phonedb数据【时间超级久】 【增量爬取】【已经开了4线程去爬取】
    爬取phonedb.net数据保存到phone_info表
2、执行nanoreviewD获取排行榜数据
    爬取nanoreview.net数据表保存到mobile_phones表【注意会先清空mobile_phones】
3、执行scParse解析android和ios数据到数据表
    【注意会清空cs_android和cs_ios表】
4、执行updateRankSQL更新排行榜
    把排行榜数据更新到cs_android和cs_ios表中
5、导出文件
    执行exportExcel 导出cs_android和cs_ios表数据


！！！ 数据库配置在mysqlConfig做统一更改