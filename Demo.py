
from fastapi import FastAPI, Depends, HTTPException,Query,Body
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=schemas.ProductResponse,status_code=201,tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=list[schemas.ProductResponse],tags=["Products"])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db=db, skip=skip, limit=limit)


@app.post("/users/", response_model=schemas.UserResponse, status_code=201,tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.UserResponse],tags=["Users"])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)

@app.post("/users/{user_id}/address", response_model=schemas.AddressResponse,status_code=201,tags=["Address"])
def add_address(user_id: int, address: schemas.AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address_for_user(db= db, user_id=user_id, address=address)


@app.get("/users/{user_id}/address", response_model=list[schemas.AddressResponse],tags=["Address"])
def get_user_addresses(user_id: int, db: Session = Depends(get_db)):
    return crud.get_addresses_by_user(db=db, user_id=user_id)

@app.post("/users/{user_id}/card", response_model=schemas.CardResponse,status_code=201,tags=["Card"])
def add_card(user_id: int, card: schemas.CardCreate, db: Session = Depends(get_db)):
    return crud.create_card_for_user(db= db, user_id=user_id, card=card)

@app.get("/users/{user_id}/card", response_model=list[schemas.CardResponse],tags=["Card"])
def get_card(user_id: int, db: Session = Depends(get_db)):
    return crud.get_card_for_user(db=db, user_id=user_id)

@app.delete("/users/{user_id}/card/{product_id}", response_model=schemas.CardResponse,tags=["Card"])
def delete_card(user_id: int, product_id: int , db: Session = Depends(get_db)):
    return crud.delete_card_for_user(db=db, user_id=user_id, product_id=product_id)

@app.patch("/card/{cart_id}", response_model=schemas.CardResponse,tags=["Card"])
def update_cart(cart_id: int, data: schemas.CartUpdate, db: Session = Depends(get_db)):
    return crud.update_cart_item(db=db, cart_id=cart_id, quantity=data.quantity)

@app.post("/login/", response_model=schemas.LoginResponse,tags=["Login"])
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.login_user(db=db, email=login_data.email, password=login_data.password)

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    if user is False:
        raise HTTPException(status_code=401, detail="Invalid password")

    return user

@app.post("/user/{user_id}/debit_card", response_model=schemas.DebitCardResponse,tags=["Debit Cards"])
def create_debit_card_for_user(user_id: int, db: Session = Depends(get_db)):
    return crud.create_debit_card(db=db, user_id=user_id)

@app.get("/user/{user_id}/debit_card", response_model=schemas.DebitCardResponse,tags=["Debit Cards"])
def get_debit_card_for_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_debit_card(db=db, user_id=user_id)

@app.delete("/user/{user_id}/debit_card/{card_id}",tags=["Debit Cards"])
def delete_debit_card_for_user(user_id: int,card_id:int ,db: Session = Depends(get_db)):
    return crud.delete_debit_card(db=db, user_id=user_id, card_id=card_id)

@app.post("/review", response_model=list[schemas.ReviewResponse],tags=["Reviews"])
def add_review(product_id:int,review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.add_review_of_product(db=db, review=review , product_id=product_id)

@app.get("/review/{product_id}",response_model=list[schemas.ReviewResponse],tags=["Reviews"])
def get_review_product(product_id:int ,db: Session = Depends(get_db)):
    return crud.get_review_of_product(db=db, product_id=product_id)

@app.put("/review/{review_id}", response_model=schemas.ReviewResponse,tags=["Reviews"])
def update_review(product_id:int,review_id:int,review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.update_review_of_product(db=db, review=review,review_id = review_id, product_id=product_id)

@app.delete("/review/{review_id}",tags=["Reviews"])
def delete_review(review_id: int, product_id: int , db: Session = Depends(get_db)):
    return crud.delete_review_of_product(db=db, review_id=review_id, product_id=product_id)

@app.post("/user/{user_id}/order", response_model=list[schemas.OrderResponse],tags=["Orders"])
def add_order(user_id: int,order: schemas.OrderCreate,db: Session = Depends(get_db)):
    return crud.place_order(db=db, user_id=user_id, order=order)

@app.get("/user/{user_id}/order", response_model=list[schemas.OrderResponse],tags=["Orders"])
def get_order(user_id: int,db: Session = Depends(get_db)):
    return crud.get_user_orders(db=db, user_id=user_id)

"""
from fastapi import FastAPI
from pydantic import BaseModel


class Product(BaseModel):
    id : int
    name : str
    price : int


app = FastAPI()

var_products = [
    {"id": 1, "name": "Iphone", "price": 45000},
    {"id": 2, "name": "Samsung", "price": 60000},
    {"id": 3, "name": "Nokia", "price": 100000}
]

@app.get("/")
def root():
    return {"message": "Hello from first API"}

@app.get("/products")
def get_product():
    return {"products": var_products}

@app.get("/products/{productid}")
def get_product_specific(productid:int):
    for product in var_products:
        if product["id"] == productid:
            return product
    return {"error": "Product not found"}


@app.post('/add_product')
def add_product(product : Product):
    # new_id = var_products[-1]["id"] + 1
    new_product = {"id": product.id, "name": product.name, "price": product.price}
    for i in var_products:
        if i["id"] == new_product["id"]:
            return ' It is Already Present '
    var_products.append(new_product)
    return {"message": "Product added", "product": new_product}

"""
