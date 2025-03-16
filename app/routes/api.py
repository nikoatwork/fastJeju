from fastapi import APIRouter, HTTPException
import pandas as pd
from app.models import Item, ItemResponse
from typing import List

router = APIRouter(prefix="/api", tags=["api"])

# --------
# EXAMPLE API ENDPOINTS
# These are example endpoints to demonstrate how to use FastAPI with pandas DataFrame
# We have on GET /items and /items/{item_id} to request data
# We have on POST /items to create a new item
# --------

# Simulate a database with pandas DataFrame
sample_data = {
    "id": [1, 2, 3],
    "name": ["Jeju Orange", "Hallasan Tea", "Black Pork"],
    "description": ["Fresh orange from Jeju Island", "Tea made from Hallasan herbs", "Famous Jeju black pork"],
    "price": [5.99, 12.50, 18.75]
}

# Create a pandas DataFrame
df = pd.DataFrame(sample_data)

@router.get("/items", response_model=ItemResponse)
async def get_items():
    """
    Get all items from the database
    """
    items = [Item(**row) for _, row in df.iterrows()]
    return ItemResponse(items=items, count=len(items))

@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """
    Get a specific item by ID
    """
    item = df[df["id"] == item_id]
    if item.empty:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    return Item(**item.iloc[0])

@router.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    """
    Create a new item
    """
    global df
    # Check if item with same ID already exists
    if not df[df["id"] == item.id].empty:
        raise HTTPException(status_code=400, detail=f"Item with ID {item.id} already exists")

    # Add new item to DataFrame
    new_row = pd.DataFrame([item.dict()])
    df = pd.concat([df, new_row], ignore_index=True)

    return item

@router.get("/pandas/info")
async def pandas_info():
    """
    Get basic information about the pandas DataFrame
    """
    info = {
        "columns": df.columns.tolist(),
        "shape": df.shape,
        "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "summary": df.describe().to_dict()
    }
    return info
