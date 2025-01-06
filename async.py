"""
The project uses uvicorn to run the server.
with the following command:

uvicorn async:app --workers 3 

To spawn 3 workers to handle the requests concurrently.
"""


import asyncio
from fastapi import FastAPI
import time
import os



app = FastAPI()

"""
The following function is being executed simultaneously by 3 different processes.
The function is being executed in seqience by each process. (same process)
"""

@app.get("/1")
async def index1():
    print(f"Start by {os.getpid()}")
    time.sleep(5)
    print(f"End")

"""
The function is being called concurrently by 3 different processes.
The execution is being called by 0, 1 and then 2rd worker but ends sometimes the 0, 2 and 1st worker.

Perfect for I/O bound operations like Database calls, API calls, etc.

When Not to use:
- When you are doing CPU bound operations like heavy computations, etc.(machine learning, data processing, etc.)
- When you are doing synchronous operations.
"""
@app.get("/2")
async def index2(call_id: int):
    print(f"Start by {os.getpid()} and  {call_id}")
    await asyncio.sleep(5)
    print(f"End with {call_id}")


"""
The function is being called concurrently by 3 different processes.
It works the same way as the previous function but it is not an async function. 
The uvicorn server will create a new process for each request when there is a blocking operation.

"""
@app.get("/3")
def index3(call_id: int):
    print(f"Start by {os.getpid()} and {call_id}")
    time.sleep(5)
    print(f"End with {call_id}")