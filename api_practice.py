from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: str | None = None


class UpdateItem(BaseModel):
    name: str | None = None
    price: float | None = None
    brand: str | None = None


@app.get("/")
def home():
    return {"Data": "Testing API"}


# uvicorn api_practice:app --reload


@app.get("/about")
def about():
    return {"It's me": "About"}


inventory = {
    1: {"name": "milk", "price": 0.99, "grocery": "netto"},
    2: {"name": "bread", "price": 1.50, "grocery": "aldi"},
    3: {"name": "eggs", "price": 2.50, "grocery": "rewe"},
}


@app.get("/get-item")
def get_item():
    return inventory


@app.get("/get-item/{item_id}")
def get_item_id(
    item_id: int = Path(description="The ID of the inventory you want to see"),
):
    return inventory[item_id]


# query parameter
@app.get("/get-by-name")
def get_by_name(name: str | None = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    # raise HTTPException(status_code=404, detail="Item name not found.")
    #                   OR
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item name not found.",
        # Use of status: status makes your FastAPI code easier to read and maintain by replacing numeric codes
        # like 404 with descriptive names like status.HTTP_404_NOT_FOUND.
    )


@app.post("/create-item")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists.")
    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(
    item_id: int = Query(
        ..., description="The item ID of the item you want to delete", ge=0
    )
):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")
    del inventory[item_id]
    return {"Success": "Item deleted successfully!"}
