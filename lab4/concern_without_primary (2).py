from pymongo import MongoClient
import threading, time, os

time_of_start = time.time()

client = MongoClient('mongodb://node_1:27017,node_2:27017,node_3:27017/?replicaSet=replset', serverSelectionTimeoutMS=30000, retryWrites=True)
db = client['mydb']
collection = db['like_counters']

def increment_likes(client_id, increments):
    for _ in range(increments):
        retries = 5
        while retries > 0:
            try:
                collection.find_one_and_update(
                    {"user_id": client_id},
                    {"$inc": {"likes": 1}},
                    write_concern={'w': 1}
                )
                break
            except Exception as e:
                retries -= 1
                time.sleep(2)

num_clients = 10
increments_per_client = 10000

threads = []
for i in range(1, num_clients + 1):
    thread = threading.Thread(target=increment_likes, args=(1, increments_per_client))
    threads.append(thread)

for thread in threads:
    thread.start()

time.sleep(5)
os.system("docker stop node_3")
for thread in threads:
    thread.join()

print("Increment completed with writeConcern=1 and Primary node switched")
print("Lasted --- %s seconds" % (time.time() - time_of_start))

