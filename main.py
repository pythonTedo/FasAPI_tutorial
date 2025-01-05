from fastapi import FastAPI, HTTPException, Path, Query
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

class Category(Enum):
    TOOLS="tools"
    CONSUMABLES = "consumables"


class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category

#to Specify non path but query parameters like /items?count=20
Selection = dict[str, str | int | float | Category | None]

items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name="Naild", price=1.99, count=100, id=2, category=Category.CONSUMABLES)

}
@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}


@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.get("/items/")
def query_items_by_params(name: str | None = None, 
                          price: float | None = None,
                          count: int | None = None,
                          category: Category | None = None) -> dict[str, Selection | list[Item]]:
    
    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count != count,
                category is None or item.category is category,
            )
        )
    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category}, 
        "selection": selection,
    }

@app.post("/")
def add_item(item: Item) -> dict[str, Item]:

    if item.id in items:
        raise HTTPException(status_code=400, detail=f"Item with {item.id} already exists")
    items[item.id] = item
    return {"added": item}

@app.delete("/items/{item_id}")
def remove_item(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_id} does not exist.")
    item = items.pop(item_id)

    return {"deleted": item}

@app.put("/items/{item_id}")
def update(
    item_id: int=Path(ge=0), # >= 0
    name: str | None = Query(default = None, min_length=1, max_length=8),
    price: float | None = Query(default = None, gt=0.0),
    count: int | None = Query(default = None, gt=0)
) -> dict[str, Item]:
    
    if item_id not in items:
        HTTPException(status_code=404, detail=f"Item with {item_id} does not exist")
    if all(info is None for info in (name, price, count)):
        raise HTTPException(status_code=400, detail="No parameers provided for update")
    
    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count

    return {"updated": item}