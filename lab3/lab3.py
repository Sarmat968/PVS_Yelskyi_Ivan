from neo4j import GraphDatabase
import threading, time

time_of_start = time.time()

URL = "neo4j+s://5639217d.databases.neo4j.io"
login = "neo4j"
password = "x2GsTVllWGM827Ky3jueQjd8tlvdgWHxn1bDH7_jmp0"
AUTH = (login, password)

driver = GraphDatabase.driver(URL, auth=AUTH)
driver.verify_connectivity()
    

def increment(increments):
    with driver.session() as session:
        for _ in range(increments):
            session.run("MATCH (i:Item_plus {id: 1}) SET i.likes = i.likes + 1")

clients_total = 10
thrds = []
start_time = time.time()

for _ in range(clients_total):
    thrd = threading.Thread(target=increment, args=(10000,))
    thrds.append(thrd)

for thrd in thrds: thrd.start()
for thrd in thrds: thrd.join()

with driver.session() as session:
    result = session.run("MATCH (i:Item_plus {id: 1}) RETURN i.likes AS likes")
    print(f"Final amount of likes --- {result.single()['likes']}")
    print("Lasted --- %s seconds" % (time.time() - time_of_start))

driver.close()

