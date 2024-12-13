from pymongo import MongoClient
import threading, time

time_of_start = time.time()

client = MongoClient('mongodb://node_1:27017,node_2:27017,node_3:27017/?replicaSet=replset')
db = client['mydb']
collection = db['like_counters']

def increment_likes(client_id, increments):
    for _ in range(increments):
        collection.find_one_and_update(
            {"user_id": client_id},
            {"$inc": {"likes": 1}},
            write_concern={'w': 'majority'}
        )

num_clients = 10
increments_per_client = 10000

threads = []
for i in range(1, num_clients + 1):
    thread = threading.Thread(target=increment_likes, args=(1, increments_per_client))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("Increment completed with writeConcern=majority and Primary node up")
print("Lasted --- %s" % (time.time() - time_of_start))
