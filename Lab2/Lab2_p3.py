import psycopg2, time
from threading import Thread

def p4():
    cur_cur = con_cur.cursor()
    for i in range(0, 10000):
        while True:
            cur_cur.execute("SELECT counter, version FROM user_count WHERE user_id = 4;")
            count, ver = cur_cur.fetchone()
            cur_cur.execute(f"UPDATE user_count SET counter = {count + 1}, version = {ver + 1} WHERE user_id = 4 and version = {ver};")
            con_cur.commit()
            count_checker = cur_cur.rowcount
            if count_checker > 0:
                break
    cur_cur.close()

con_cur = psycopg2.connect("host=127.0.0.1 dbname=mdb user=ivan password=qwerty port=5432")
cur_cur = con_cur.cursor()
cur_cur.execute(f'UPDATE user_count SET counter = 0 WHERE user_id = 4;')
cur_cur.execute(f'UPDATE user_count SET version = 0 WHERE user_id = 4;')
con_cur.commit()
cur_cur.close()
        
time_of_start = time.time()
threads = [Thread(target = p4) for i in range(10)]
for thread in threads: thread.start()
for thread in threads: thread.join()
        
print("Lasted --- %s" % (time.time() - time_of_start))

cur_cur = con_cur.cursor()
cur_cur.execute(f"SELECT counter FROM user_count WHERE user_id = 3;")
print(f'count = {cur_cur.fetchone()[0]}')
    
cur_cur.close()
con_cur.close()

