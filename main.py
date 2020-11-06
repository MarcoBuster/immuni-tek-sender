from src import immuni
import botogram
import config
from datetime import datetime as dt
import base64
import time
import sqlite3


def _ts_to_human(ts):
    ts_dt = dt.fromtimestamp(ts)
    return f"{ts_dt.day:02d}/{ts_dt.month:02d}/{ts_dt.year} {ts_dt.hour:02d}:{ts_dt.minute:02d}:{ts_dt.second:02d}"


bot = botogram.create(config.BOT_TOKEN)
imm = immuni.ImmuniAPI()
conn = sqlite3.connect("seen.sqlite")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS seen(batch_num INTEGER PRIMARY KEY)")


def send_batch(batch_num):
    b = imm.get_batch(batch_num)

    text = (
        "❗️ <b>Nuovi batch chiavi aggiunto</b>"
        f"\n🔢 <b>Batch #{batch_num}</b>"
        f"\n🗓 <b>Periodo ricezione</b>: "
        f"{_ts_to_human(b.start_timestamp)} - {_ts_to_human(b.end_timestamp)}"
        f"\n🔑 <b>Numero chiavi</b>: {len(b.keys)}"
    )
    for i, k in enumerate(b.keys):
        text += f"\n➖ <code>{base64.b64encode(k.key_data).decode('utf-8')}</code>"
        if i > 50:
            text += f"\n<i>(...e altre)</i>"

    bot.chat(config.DEST_CHANNEL).send(text, syntax="html")


if __name__ == "__main__":
    indx = imm.index()
    for num in range(indx["oldest"], indx["newest"]+1):
        c.execute("SELECT 1 FROM seen WHERE batch_num=?", (num ,))
        res = c.fetchone()
        if res:
            print('Skipped', num)
            continue
        c.execute("INSERT INTO seen VALUES(?)", (num,))
        conn.commit()

        send_batch(num)
        print('Sent', num)
        time.sleep(5)
    conn.close()
