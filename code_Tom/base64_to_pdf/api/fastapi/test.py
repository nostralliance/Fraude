from fastapi import FastAPI
import uvicorn

app = FastAPI()

products = [
    {"id": 1, "name": "iPad", "price": 599},
    {"id": 2, "name": "iPhone", "price": 999},
    {"id": 3, "name": "iWatch", "price": 699},
]

@app.get("/")
def index():
    return {"data": "test"}


# Cette fonctions permet de renvoyer tout les articles dans notre fake BDD
@app.get("/products")
def product():
    return products

# Ici cette fonction nous permet de ressortir le produit en fonction de l'ID
@app.get("/products/{id}")
def index(id: int):
    for product in products:
        if product["id"] == id:
            return product
    return "Not found" 


if __name__ == '__main__':
    uvicorn.run(app)
    