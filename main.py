import sqlite3
conn = sqlite3.connect("DB.db")
cursor = conn.cursor()

mes = 'message'

cursor.execute("""CREATE TABLE IF NOT EXISTS messages (PID INTEGER PRIMARY KEY AUTOINCREMENT, 
            text VARCHAR(100))""")

cursor.execute(f"""INSERT INTO messages (text) VALUES('{mes}')""")

cursor.execute("SELECT * FROM messages")
rows = cursor.fetchall()

for row in rows:
    for col in row:
        print(col)
