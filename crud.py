import datetime
from statistics import quantiles
from Pass import hash_password, verify_password
from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException
from cards import generate_card


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        isInsured=product.isInsured
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed = hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password = hashed,
        confirm_password = hashed
    )
    # Password validation
    if user.password != user.confirm_password:
        return {"error": "Passwords do not match"}

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_address_for_user(db: Session, user_id: int, address: schemas.AddressCreate):
    exisiting_user=db.query(models.User).filter(user_id==models.User.id).first()
    print(exisiting_user)
    if exisiting_user is not None:
        db_address = models.Address(
            user_id=user_id,
            address=address.address,
            pincode=address.pincode,
            state=address.state,
            city=address.city,
            country=address.country
        )
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    else:
        raise HTTPException(status_code=404 ,detail=f"User id :- {user_id} Does Not Exist")

def get_addresses_by_user(db: Session, user_id: int):
    return db.query(models.Address).filter(models.Address.user_id == user_id).all()


def create_card_for_user(db: Session, user_id: int, card: schemas.CardCreate):
    exisiting_user=db.query(models.User).filter(models.User.id==user_id).first()
    product_avaliable=db.query(models.Product).filter(models.Product.id==card.product_id).first()
    print(exisiting_user)
    print(product_avaliable)
    if product_avaliable is None:
        raise HTTPException(status_code=404, detail=f'Given Product is not Avaliable')
    if exisiting_user is None :
        raise HTTPException(status_code=404, detail=f'Given Users is not Avaliable')
    if product_avaliable.quantity <= 0:
        raise HTTPException(status_code=404, detail=f'Given Product Out of Stock')
    if product_avaliable.quantity < card.quantity:
        raise HTTPException(status_code=404, detail=f'Given Product only available {product_avaliable.quantity}')
    db_card = models.Card(
        user_id=user_id,
        product_id = card.product_id,
        quantity = card.quantity
    )
    db.add(db_card)
    product_avaliable.quantity-=card.quantity
    db.add(product_avaliable)
    db.commit()
    db.refresh(db_card)
    return db_card

def get_card_for_user(db: Session, user_id: int):
    return db.query(models.Card).filter(models.Card.user_id == user_id).all()

def delete_card_for_user(db: Session, user_id: int,product_id:int):
    user = db.query(models.Card).filter(models.Card.user_id == user_id).all()
    if user is None:
        raise HTTPException(status_code=404, detail=f'Given Users is not Avaliable')
    products = db.query(models.Product).filter(models.Product.id == product_id).all()
    if products is None:
        raise HTTPException(status_code=404, detail=f'Given products is not Avaliable')
    product_avaliable=db.query(models.Product).filter(models.Product.id==models.Card.product_id).first()

    card = (
        db.query(models.Card)
        .filter(models.Card.user_id == user_id, models.Card.product_id == product_id)
        .first()
    )
    product_avaliable.quantity += card.quantity
    db.delete(card)
    db.commit()
    raise HTTPException(status_code=200, detail=f'Data Not Found')

def update_cart_item(db: Session, cart_id: int, quantity: int):

    # 1. Get cart item
    cart_item = db.query(models.Card).filter(models.Card.id == cart_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    # 2. Get product
    product = db.query(models.Product).filter(models.Product.id == cart_item.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 3. Calculate difference
    old_qty = cart_item.quantity
    new_qty = quantity
    difference = new_qty - old_qty  # +ve = increase, -ve = decrease

    # 4. Increase quantity → reduce stock
    if difference > 0:
        if product.quantity < difference:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock available"
            )
        product.quantity -= difference

    # 5. Decrease quantity → increase stock
    elif difference < 0:
        product.quantity += abs(difference)

    # 6. Update cart
    cart_item.quantity = new_qty
    db.commit()
    db.refresh(cart_item)

    return cart_item

def login_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None

    if not verify_password(user.password, password):
        return False

    return user

def create_debit_card(db: Session, user_id: int):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_card = db.query(models.DebitCard).filter(models.DebitCard.user_id == user_id).first()
    if existing_card:
        raise HTTPException(status_code=400, detail="Debit card already exists for this user")

    card_data = generate_card()  # no balance here

    debit_card = models.DebitCard(
        user_id=user_id,
        card_number=card_data["card_number"],
        cvv=card_data["cvv"],
        expiry=card_data["expiry"],
        balance=card_data['balance']
    )

    db.add(debit_card)
    db.commit()
    db.refresh(debit_card)

    return debit_card

def get_debit_card(db: Session, user_id: int):

    debit_card = db.query(models.DebitCard).filter(
        models.DebitCard.user_id == user_id
    ).first()

    if not debit_card:
        raise HTTPException(
            status_code=404,
            detail="Debit card not found for this user"
        )

    return debit_card

def delete_debit_card(db: Session, user_id: int, card_id: int):
    debit_card = db.query(models.DebitCard).filter(models.DebitCard.id == card_id,models.DebitCard.user_id == user_id).first()
    if not debit_card:
        raise HTTPException(status_code=404,
            detail="Debit card not found for this user"
        )
    db.delete(debit_card)
    db.commit()

    return {"message": "Debit card deleted successfully"}
def add_review_of_product(db: Session, review: schemas.ReviewCreate,product_id:int):
    user = db.query(models.User).filter(
        models.User.id == review.user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")


    db_review = models.Review(
        user_id=review.user_id,
        product_id=product_id,
        heading=review.heading,
        description=review.description,
        rating=review.rating,
        user_name=user.name,
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_review_of_product(db: Session, product_id: int):
    db_review = db.query(models.Review).filter(
        models.Review.product_id == product_id
    ).all()
    return db_review

def update_review_of_product(
    db: Session,
    review: schemas.ReviewCreate,
    review_id: int,
    product_id: int
):
    db_review = db.query(models.Review).filter(models.Review.id == review_id,models.Review.product_id == product_id).first()

    if not db_review:
        raise HTTPException(
            status_code=404,
            detail="Review not found for this product"
        )

    if db_review.user_id != review.user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to update this review"
        )

    db_review.heading = review.heading
    db_review.description = review.description
    db_review.rating = review.rating

    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review_of_product(db: Session,review_id: int,product_id: int):
    db_review = db.query(models.Review).filter(models.Review.id == review_id,models.Review.product_id == product_id).first()

    if not db_review:
        raise HTTPException(
            status_code=404,
            detail="Review not found for this product"
        )

    db.delete(db_review)
    db.commit()

    return {"message": "Review deleted successfully"}

def place_order(db: Session, user_id: int, order: schemas.OrderCreate):
    cart_items = db.query(models.Card).filter(models.Card.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    address = db.query(models.Address).filter(models.Address.id == order.address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    debit_card = None
    if order.card_id:
        debit_card = db.query(models.DebitCard).filter(
            models.DebitCard.id == order.card_id,
            models.DebitCard.user_id == user_id
        ).first()
        if not debit_card:
            raise HTTPException(status_code=404, detail="Debit card not found")

    orders_created = []

    try:
        for item in cart_items:
            product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

            total_amount = product.price * item.quantity

            if debit_card:
                if debit_card.balance < total_amount:
                    raise HTTPException(status_code=400, detail="Insufficient balance")
                debit_card.balance -= total_amount

            new_order = models.Order(
                user_id=user_id,
                product_id=product.id,
                address_id=address.id,
                card_id=debit_card.id if debit_card else None,
                quantity=item.quantity,
                total_amount=total_amount,
                status="PLACED"
            )
            db.add(new_order)
            db.commit()
            db.refresh(new_order)

            order_response = schemas.OrderResponse(
                id=new_order.id,
                address_id=new_order.address_id,
                card_id=str(new_order.card_id) if new_order.card_id else None,
                user_id=new_order.user_id,
                quantity=new_order.quantity,
                total_amount=new_order.total_amount,
                status=new_order.status
            )
            orders_created.append(order_response)

        db.query(models.Card).filter(models.Card.user_id == user_id).delete()
        db.commit()

        return orders_created

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_user_orders(db: Session, user_id: int) -> list[schemas.OrderResponse]:
    orders = db.query(models.Order).filter(models.Order.user_id == user_id).all()
    if not orders:
        return []

    order_list = []
    for order in orders:
        order_response = schemas.OrderResponse(
            id=order.id,
            address_id=order.address_id,
            card_id=str(order.card_id) if order.card_id else None,
            user_id=order.user_id,
            quantity=order.quantity,
            total_amount=order.total_amount,
            status=order.status
        )
        order_list.append(order_response)

    return order_list