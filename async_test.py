import requests
import threading
import time

start = time.time()
workers = 3

for i in range(workers):
    #threading.Thread(target=requests.get, args=(f"http://localhost:8000/2?call_id={i}",)).start()
    threading.Thread(target=requests.get, args=(f"http://localhost:8000/3?call_id={i}",)).start()
stop = time.time()

print(f"Time taken: {stop-start}")