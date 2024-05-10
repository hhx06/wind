import pymysql


def is_prefix(text, prefix):
    return text[:len(prefix)] == prefix


# MySQL 连接信息
host = '10.18.40.214'
user = 'root'
password = 'root000'
database = 'phone'

# 连接到 MySQL 数据库
conn = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = conn.cursor()

# 执行 SELECT 查询
select_query = "SELECT id, codeName,model FROM phone_info WHERE id >0"
cursor.execute(select_query)

# 获取查询结果
results = cursor.fetchall()

# 遍历结果并进行处理
for row in results:
    id1, codeName, model = row
    # 进行某些处理，例如将 age 增加 1
    codeName_trim1 = str(codeName).replace(" ", "")
    model_trim1 = str(model).replace(" ", "")
    # 执行 UPDATE 查询更新字段
    # 如果是前缀是Apple  去掉前缀
    if is_prefix(codeName_trim1, "Apple"):
        codeName_trim1 = codeName_trim1[5:]
    update_query = "UPDATE phone_info SET codeName_trim = %s , model_trim = %s WHERE id = %s"
    # update_query = f"-- UPDATE phone_info SET codeName_trim = {codeName_trim1} , model_trim = {model_trim1} WHERE
    # id = {id1}"

    cursor.execute(update_query, (codeName_trim1, model_trim1, id1))

# 提交事务
conn.commit()

# 关闭游标和连接
cursor.close()
conn.close()
