import sqlite3

conn = sqlite3.connect("data/app.db")

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users(
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        bio CHAR NOT NULL,
        pic TEXT NOT NULL
        )""")
conn.commit()
conn.close()