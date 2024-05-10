import pymysql
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from phoneRankDataParse import mysqlConfig


# 创建 MySQL 数据表
def create_table(mysqlData):
    # 连接到 MySQL 数据库
    conn = pymysql.connect(host=mysqlData[0], user=mysqlData[1], password=mysqlData[2], database='phone')
    # 创建一个游标对象
    cursor = conn.cursor()
    # mobile_phones
    cursor.execute("SHOW TABLES LIKE 'mobile_phones'")
    table_exists = cursor.fetchone()
    # 如果存在，则先删除该表
    if table_exists:
        cursor.execute("DROP TABLE mobile_phones")
    # 创建表的 SQL 语句
    sql = """CREATE TABLE IF NOT EXISTS mobile_phones (
                 id INT AUTO_INCREMENT PRIMARY KEY,
                 rank INT,
                 name VARCHAR(255),
                 company VARCHAR(255),
                 score FLOAT,
                 rating VARCHAR(255),
                 antutu INT,
                 gkb INT,
                 core INT,
                 clock VARCHAR(255),
                 gpu VARCHAR(255),
                 model_id INT
             )"""

    # 执行 SQL 语句
    cursor.execute(sql)

    # 提交事务
    conn.commit()

    # 关闭游标和连接
    cursor.close()
    conn.close()


# 插入数据到 MySQL 数据表
def insert_to_db(data, mysqlData):
    # 连接到 MySQL 数据库
    conn = pymysql.connect(host=mysqlData[0], user=mysqlData[1], password=mysqlData[2], database='phone')
    # 创建一个游标对象
    cursor = conn.cursor()

    # 插入数据的 SQL 语句
    sql = """INSERT INTO mobile_phones (rank, name, company, score, rating, antutu, gkb, core, clock, gpu, model_id)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    # 执行 SQL 语句
    cursor.execute(sql, data)

    # 提交事务
    conn.commit()

    # 关闭游标和连接
    cursor.close()
    conn.close()


# 根据名称模糊匹配 phone_info 表中的 model 字段，并获取 id
def get_model_id(name):
    conn = pymysql.connect(host='10.18.40.214', user='root', password='root000', database='phone')
    cursor = conn.cursor()
    sql = "SELECT id FROM phone_info WHERE cpu LIKE %s"
    cursor.execute(sql, ("%" + name + "%",))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    else:
        return None


def data(url, mysqlData):
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析页面内容
        soup = BeautifulSoup(response.text, "html.parser")
        soups = soup.tbody('tr')
        for soup in soups:
            td_list = soup.find_all("td")
            rank = soup.find("div", class_="table-list-order").get_text().strip()
            name = soup.find("a").get_text().strip()
            company = soup.find("span", class_="text-gray-small").get_text()
            score = soup.find("div", class_="table-list-score-box").get_text().strip()
            rating = soup.find("div", class_="table-list-score-box").parent.span.get_text().strip()
            antutu = td_list[3].get_text().strip()
            gkb = td_list[4].get_text().strip()
            core = soup.find("div", class_="table-list-custom-circle").get_text().strip()
            clock = td_list[6].get_text().strip()
            gpu = td_list[7].get_text().strip()
            # 获取模糊匹配到的 model 字段对应的 id
            # model_id = get_model_id(name)
            # 插入数据库
            data1 = (rank, name, company, score, rating, antutu, gkb, core, clock, gpu)
            insert_to_db(data1, mysqlData)
    else:
        print("Failed to retrieve the webpage.")


def main():
    mysqlData = mysqlConfig.get_mysql_config()
    if len(mysqlData) < 3:
        return
    url = "https://nanoreview.net/en/soc-list/rating"
    # 创建数据表
    create_table(mysqlData)
    data(url, mysqlData)
    # 使用线程池并发请求页面内容并插入数据库
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     executor.map(data, [url] * 2)


if __name__ == "__main__":
    main()
