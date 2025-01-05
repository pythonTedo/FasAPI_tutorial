import requests

#print(requests.get("http://localhost:8000/items/1").json())

#print(requests.get("http://localhost:8000/items?name=Naild").json())

print(
    requests.post("http://localhost:8000",
    json={"name": "Screwdriver",
    "price": 3.99, 
    "count": 10, 
    "id": 4, 
    "category": "tools"}).json()
)
print("------------------------------------------------------------------")
print(requests.delete("http://localhost:8000/items/1").json())
print(requests.get("http://localhost:8000").json())

print("------------------------------------------------------------------")
print(requests.put("http://localhost:8000/items/0?count=9001&name=Demo").json())
print(requests.get("http://localhost:8000").json())