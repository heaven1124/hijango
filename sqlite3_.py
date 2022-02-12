import sqlite3

# sqlite3是一个微型数据库，主要用于浏览器、平板、手机等智能设备的应用
# 支持标准的SQL语句，不过没有特定的数据类型，可以根据开发语言的特性，
# 来限定字段的类型---手机的数据都存在sqlite3中
conn = sqlite3.connect('users.sqlite3') # 文件不存在会自动创建
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE user(id INTEGER PRIMARY KEY , name, age, phone)
""")
cursor.execute("""
    INSERT INTO user(name, age, phone)
    values ('sl', 20, '18888888888')
""")
cursor.execute("""
    INSERT INTO user(name, age, phone)
    values ('zh', 11, '19999999999')
""")
cursor.execute("SELECT * from user ")
for row in cursor.fetchall():
    print(row)

conn.commit()