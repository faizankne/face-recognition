import mysql.connector

conn = mysql.connector.connect(user='root', password='root', host='localhost', database='face_recoginition', port=3306)
cursor = conn.cursor()

cursor.execute("SHOW DATABASES")

data = cursor.fetchall()

print(data)

conn.close()
