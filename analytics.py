from src import immuni
import sqlite3

imm = immuni.ImmuniAPI()
conn = sqlite3.connect("analytics.sqlite")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS analytics(batch_num INTEGER PRIMARY KEY, end_timestamp DATETIME, keys INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS seen(batch_num INTEGER PRIMARY KEY)")

# Fetch unseen batches
indx = imm.index()
for num in range(1, indx["newest"]+1):
    c.execute("SELECT 1 FROM seen WHERE batch_num=?", (num, ))
    res = c.fetchone()
    if res:
        print("Skipped", num)
        continue
    b = imm.get_batch(num)
    c.execute("INSERT INTO seen VALUES(?)", (num, ))
    if not b:
        print("Not found (too old)", num)
        continue
    c.execute("INSERT INTO analytics VALUES(?, ?, ?)", (num, b.end_timestamp, len(b.keys)))
    print("Added", num, b.end_timestamp, len(b.keys))

conn.commit()
conn.close()

