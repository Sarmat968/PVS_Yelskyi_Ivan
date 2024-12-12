import psycopg2, time
from threading import Thread

def p1():        
    cur_cur = con_cur.cursor()    
    for i in range(0, 10000):
        cur_cur.execute("SELECT counter FROM user_count WHERE user_id = 1;")
        count = cur_cur.fetchone()[0]
        count += 1
        cur_cur.execute(f"UPDATE user_count SET counter = {count} WHERE user_id = 1;")
        con_cur.commit()        
    cur_cur.close()
    
def p2():
    cur_cur = con_cur.cursor()
    for i in range(0, 10000):
        cur_cur.execute("UPDATE user_count SET counter = counter + 1 WHERE user_id = 2;")
        con_cur.commit()
    cur_cur.close() 

con_cur = psycopg2.connect("host=127.0.0.1 dbname=mdb user=ivan password=qwerty port=5432")
cur_cur = con_cur.cursor()
cur_cur.execute(f'UPDATE user_count SET counter = 0 WHERE user_id = 2;')
con_cur.commit()
cur_cur.close()
        
time_of_start = time.time()
threads = [Thread(target = p2) for i in range(10)]
for thread in threads: thread.start()
for thread in threads: thread.join()
        
print("Lasted --- %s" % (time.time() - time_of_start))

cur_cur = con_cur.cursor()
cur_cur.execute(f"SELECT counter FROM user_count WHERE user_id = 2;")
print(f'count = {cur_cur.fetchone()[0]}')
    
cur_cur.close()
con_cur.close()

