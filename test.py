import pymysql

connection = pymysql.connect(host='sql11.freesqldatabase.com',
                             user='sql11189251',
                             password='bEzYRY6iRP',
                             db='sql11189251',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor();
sql_query = "INSERT INTO categories (name) VALUES ('test2')"
cursor.execute(sql_query)
connection.commit()
result = cursor.lastrowid
print(result)