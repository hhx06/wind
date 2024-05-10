import time

import pymysql
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from phoneRankDataParse import mysqlConfig


# 获取最大页码数
def max_num(url):
    max_page = 0
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析页面内容
        soup = BeautifulSoup(response.text, "html.parser")
        # 查找包含指定范围的链接文本的<a>标签
        links = soup.find_all("a", href=True, title=True)
        # 遍历每个链接
        for link in links:
            # 检查链接文本是否包含指定范围
            if "Jump to page" in link["title"]:
                # print("Target URL:", link.get_text())
                if "-" in link.get_text():
                    page_range = link.get_text().split("-")
                    if len(page_range) > 1:
                        max_page = page_range[1]

    else:
        print("Failed to retrieve the webpage.")
    return max_page


def page_content(url, page_num, mysqlData):
    response = requests.get(url + str(page_num))
    print("url:", url + str(page_num))
    # 检查请求是否成功
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析页面内容
        response_text = response.text
        brand = extract_info(response_text, "1")
        model = extract_info(response_text, "2")
        codeName = extract_info(response_text, "6")
        released = extract_info(response_text, "10")
        cpu_clock = extract_info(response_text, "37")
        cpu = extract_info(response_text, "36")
        gpu_clock = extract_info(response_text, "149")
        gpu = extract_info(response_text, "147")
        resolution = extract_info(response_text, "91")
        display_diagonal = extract_info(response_text, "86")
        ram = extract_info(response_text, "23")
        dimensions = extract_info(response_text, "49")
        # 插入数据库
        insert_to_db(page_num, brand, model, codeName, released, cpu_clock, cpu, gpu_clock, gpu, resolution,
                     display_diagonal, ram, dimensions, mysqlData)
    else:
        print("Failed to retrieve the webpage.")


# 提取到的信息
def extract_info(response, item_id):
    soup = BeautifulSoup(response, "html.parser")
    item_td = soup.find("a", id="datasheet_item_id" + item_id)
    if item_td:
        return item_td.parent.get_text()
    else:
        return None


def create_table(mysqlData):
    # 连接到 MySQL 数据库
    conn = pymysql.connect(host=mysqlData[0], user=mysqlData[1], password=mysqlData[2], database='phone')
    # 创建一个游标对象
    cursor = conn.cursor()
    # # 检查是否存在phone_info表
    # cursor.execute("SHOW TABLES LIKE 'phone_info'")
    # table_exists = cursor.fetchone()
    # # 如果存在，则先删除该表
    # if table_exists:
    #     cursor.execute("DROP TABLE phone_info")
    # 创建表的 SQL 语句
    sql = """CREATE TABLE IF NOT EXISTS phone_info (
                 id INT AUTO_INCREMENT PRIMARY KEY,
                 page_num INT,
                 brand VARCHAR(255),
                 model VARCHAR(255),
                 codeName VARCHAR(255),
                 released VARCHAR(255),
                 cpu_clock VARCHAR(255),
                 cpu VARCHAR(255),
                 gpu_clock VARCHAR(255),
                 gpu VARCHAR(255),
                 resolution VARCHAR(255),
                 display_diagonal VARCHAR(255),
                 ram VARCHAR(255),
                 dimensions VARCHAR(255),
                 nanoreview_id INT,
                 codeName_trim VARCHAR(255),
                 model_trim VARCHAR(255)
             )"""

    # 执行 SQL 语句
    cursor.execute(sql)

    # 提交事务
    conn.commit()

    # 关闭游标和连接
    cursor.close()
    conn.close()


def is_prefix(text, prefix):
    return text[:len(prefix)] == prefix


def get_max_page_num(mysqlData):
    # 连接到 MySQL 数据库
    conn = pymysql.connect(host=mysqlData[0], user=mysqlData[1], password=mysqlData[2], database='phone')
    # 创建一个游标对象
    cursor = conn.cursor()
    query_sql = f"SELECT page_num FROM phone_info  order by page_num desc limit 1"
    cursor.execute(query_sql)
    result = cursor.fetchone()
    # 提交事务
    conn.commit()
    # 关闭游标和连接
    cursor.close()
    conn.close()
    if len(result) > 0:
        return result[0]


def insert_to_db(page_num, brand, model, codeName, released, cpu_clock, cpu, gpu_clock, gpu, resolution,
                 display_diagonal, ram, dimensions, mysqlData):
    # 连接到 MySQL 数据库
    conn = pymysql.connect(host=mysqlData[0], user=mysqlData[1], password=mysqlData[2], database='phone')
    # 创建一个游标对象
    cursor = conn.cursor()
    # 进行某些处理，例如将 age 增加 1
    codeName_trim1 = str(codeName).replace(" ", "")
    model_trim1 = str(model).replace(" ", "")
    if is_prefix(codeName_trim1, "Apple"):
        codeName_trim1 = codeName_trim1[5:]
    # 插入数据的 SQL 语句
    sql = """INSERT INTO phone_info (page_num, brand, model, codeName, released, cpu_clock, cpu, gpu_clock, gpu, resolution, display_diagonal, ram, dimensions,nanoreview_id,codeName_trim,model_trim)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"""
    if len(brand) > 0:
        # 执行 SQL 语句
        cursor.execute(sql, (
            page_num, brand, model, codeName, released, cpu_clock, cpu, gpu_clock, gpu, resolution, display_diagonal,
            ram,
            dimensions, 0, codeName_trim1, model_trim1))

    # 提交事务
    conn.commit()

    # 关闭游标和连接
    cursor.close()
    conn.close()


def main():
    mysqlData = mysqlConfig.get_mysql_config()
    if len(mysqlData) < 3:
        return
    # 发送 GET 请求获取页面内容
    url = "https://phonedb.net/index.php?m=device&s=list"
    content_url = "https://phonedb.net/index.php?m=device&id="
    max_page = max_num(url)
    print("最大的数据码为:", max_page)
    if int(max_page) > 0:
        # 创建数据表
        create_table(mysqlData)
        # 先查出之前最大page_num
        max_page_num = get_max_page_num(mysqlData)
        print("现有最大的:", max_page_num)
        if int(max_page) > int(max_page_num):
            # 使用线程池并发请求页面内容并插入数据库
            with ThreadPoolExecutor(max_workers=4) as executor:
                time.sleep(2)
                executor.map(page_content, [content_url] * int(max_page),
                             range(int(max_page_num) + 1, int(max_page) + 1), mysqlData)


if __name__ == "__main__":
    main()
