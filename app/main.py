from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os

app = FastAPI()

# Serve static files (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve images
app.mount("/images", StaticFiles(directory="images"), name="images")

STOCK_FILE = "app/stock.json"

def read_stock():
    with open(STOCK_FILE, "r") as f:
        return json.load(f)

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/stock/{item_code}")
def get_stock(item_code: str):
    data = read_stock()
    item = data.get(item_code.upper())

    if not item:
        return {"error": "Item not found"}

    return {
        "item_code": item_code.upper(),
        "name": item["name"],
        "stock": item["stock"],
        "image_url": f"/images/{item['image']}"
    }
