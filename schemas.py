from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
    isInsured: bool

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name : str
    email : str
    phone : int
    password : str
    confirm_password : str

class UserResponse(UserCreate):
    id: int
    # user_id : int

    class Config:
        orm_mode = True


class AddressCreate(BaseModel):
    address: str
    pincode: str
    state: str
    city: str
    country: str

class AddressResponse(AddressCreate):
    id: int

    class Config:
        orm_mode = True

class CardCreate(BaseModel):
    product_id : int
    quantity : int = 1

class CardResponse(CardCreate):
    id: int

    class Config:
        orm_mode = True


class CartUpdate(BaseModel):
    quantity: int


class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: int

    class Config:
        orm_mode = True

class DebitCardCreate(BaseModel):
    user_id: int
    card_number: str
    cvv: str
    expiry: str
    balance: float
class DebitCardResponse(DebitCardCreate):
    id : int

    class Config:
        orm_mode = True

class ReviewCreate(BaseModel):
    user_id : int
    heading : str
    description : str
    rating : float


class ReviewResponse(ReviewCreate):
    id: int
    user_id: int
    product_id: int
    heading: str
    description: str
    rating: float
    user_name: str

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    address_id: int
    card_id: int   # send 0 or null if COD

class OrderResponse(BaseModel):
    id: int
    address_id : int
    card_id : str
    user_id : int
    quantity: int
    total_amount: float
    status: str

    class Config:
        orm_mode = True


