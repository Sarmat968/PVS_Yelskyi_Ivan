import hazelcast
from threading import Thread, Lock
import time



client_haze = hazelcast.HazelcastClient(cluster_name="custom_cluster") 
map_haze = client_haze.get_map("Custom_IMap").blocking() 

def p1():
    count = 0    
    threadLock = Lock()
    key = "p1"    
    for i in range(10000):
        with threadLock:
            count += 1
            map_haze.put(key, count)

def p2():
    key = "p2"
    if (not map_haze.contains_key(key)): map_haze.put(key, 0)    
    for i in range(10000):
        count = map_haze.get(key)        
        count += 1        
        map_haze.put(key, count)
        

def p3():
    key = "p3"
    if (not map_haze.contains_key(key)):
        map_haze.put(key, 0)        
    for i in range(10000):
       map_haze.lock(key)       
       try:
           count = map_haze.get(key)
           count += 1
           map_haze.put(key, count)            
       finally:
           map_haze.unlock(key)
           

def p4():
    key = "p4"
    if (not map_haze.contains_key(key)): map_haze.put(key, 0)     
    for i in range(10000):
        while True:
            count = map_haze.get(key)            
            count_ = count
            count_ += 1
            
            if (map_haze.replace_if_same(key, count, count_)):
                break
                
                
thrds = [Thread(target = p4) for i in range(10)]

time_of_start = time.time()

for thrd in thrds: thrd.start()
for thrd in thrds: thrd.join()

print("Lasted --- %s" % (time.time() - time_of_start))

