import hazelcast, time
from threading import Thread, Lock



client_haze = hazelcast.HazelcastClient(cluster_name="custom_cluster") 
map_haze = client_haze.get_map("Custom_IMap").blocking() 


def p5():
    count = hz_client.cp_subsystem.get_atomic_long("counter").blocking()
    counter = 0    
    count.set(0)    
    for i in range(10000):
        counter = count.add_and_get(1)


thrds = [Thread(target = p5) for i in range(10)]

time_of_start = time.time()

for thrd in thrds: thrd.start()
for thrd in thrds: thrd.join()

print("Lasted --- %s" % (time.time() - time_of_start))
