from coupon import Coupon
from review import Review
from controller import Controller

from pydantic import BaseModel 

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import uvicorn


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get('/index/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)

static_directory = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_directory, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_directory), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

controller = Controller()
controller.add_user('tur', "customer", "123")
controller.add_user('tart', "customer", "234")
controller.add_user('turadmin', "shop", "admin")
controller.add_user('tartadmin', "shop", "admin")
controller.add_user('iceadmin', "shop", "admin")
controller.add_user('nutadmin', "shop", "admin")


Turacc = controller.search_account_by_name("tur")
Tartacc = controller.search_account_by_name("tart")

shop1 = controller.add_shop(101)
shop2 = controller.add_shop(102)
shop3 = controller.add_shop(103)
shop4 = controller.add_shop(104)

shopacc101 = controller.search_account_by_name("turadmin")
shopacc101.set_branch(101)
shopacc102 = controller.search_account_by_name("tartadmin")
shopacc102.set_branch(102)
shopacc103 = controller.search_account_by_name("iceadmin")
shopacc103.set_branch(103)
shopacc104 = controller.search_account_by_name("nutadmin")
shopacc104.set_branch(104)

controller.add_pizza('pepperoni', 100)
controller.add_pizza('margherita', 120)
controller.add_pizza('hawaiian', 150)
controller.add_pizza('cheese', 150)
controller.add_drink('coke', 12)
controller.add_drink('weed', 15)
controller.add_drink('water', 10)
controller.add_pizza('A', 9999)

Turacc.basket.add_pizza(controller.create_pizza_item("pepperoni", "L", 2))
Turacc.basket.add_pizza(controller.create_pizza_item("pepperoni", "L", 2))
Turacc.basket.add_pizza(controller.create_pizza_item("margherita", "M", 1))
Turacc.basket.add_drink(controller.create_drink_item("coke", "M", 3))


controller.add_coupon(Coupon("ABC123", 10, "2024-12-31"))
controller.add_coupon(Coupon("DEF456", 20, "2025-02-28"))
controller.add_coupon(Coupon("GHI789", 30, "2022-12-31"))
controller.add_coupon(Coupon('TEST', 100000, "2025-01-01"))

controller.add_coupon_to_account(controller.get_user_id_by_name('tur'), "ABC123")
controller.add_coupon_to_account(controller.get_user_id_by_name('tur'), "DEF456")

Turacc.create_order()
controller.confirm_order(controller.get_user_id_by_name('tur'), "Delivery", "123/4", 101, "cash")
controller.process_payment(controller.get_user_id_by_name('tur'))

Turacc.add_review(Review(5, 'good'))
Turacc.add_review(Review(3, 'not bad'))
Turacc.add_review(Review(1, 'mai aroi loey'))
Tartacc.add_review(Review(4, 'delicious pizza'))


class loginDTO(BaseModel):
    username: str
    password: str


@app.get('/')
def index(request: Request):
    return RedirectResponse(url="/docs")

@app.post('/login/', tags=["user"])
async def login(user:loginDTO) -> dict:
    account = controller.search_account_by_name(user.username)
    if account:
        if account.password == user.password:
            id = account.user.id
            role = account.user.role
            return {'status': 'success', 'token' : id, 'role': role}
        else:
            return {"message" : "password incorect"}
    else:
        return {"message" : "login failed" }
    
@app.post('/register/', tags=["user"])
async def register(user:loginDTO) -> dict:
    if controller.search_account_by_name(user.username):
        return {"message" : "user name already exist" }
    controller.add_user(user.username, "customer", user.password)
    return {'status': 'success'}

@app.get('/basket/', tags=["basket"])
def get_basket(token: str) -> dict:
    account = controller.search_account_by_user_id(token)
    if account != None :
        if account.basket :
            return account.basket.to_dict()
        else: 
            return {"message" : "Basket not found"}
    return {"message" : "User not found"}
    

@app.post('/basket/add_pizza/', tags=["basket"])
def add_pizza_to_basket(token: str, face: str, size: str, quantity: int) -> dict:
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}
    account.basket.add_pizza(controller.create_pizza_item(face, size, quantity))
    return account.basket.to_dict()

@app.post('/basket/add_drink/', tags=["basket"])
def add_drink_to_basket(token: str, name: str, size: str, quantity: int) -> dict:
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}
    account.basket.add_drink(controller.create_drink_item(name, size, quantity))
    return account.basket.to_dict()

@app.get('/order/', tags=["order"])
def get_order_list(token: str) -> dict:
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}
    return {'order_list': 
            [order.to_dict() for order in account.completed_order_list]}

@app.get('/current_order/', tags=["order"])
def get_current_order(token: str) -> dict:
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}
    if account.uncompleted_order == None:
        return {"message" : "No current order"}
    return account.uncompleted_order.to_dict()
    
@app.post('/create_order/', tags=["order"])
def create_order(token: str) -> dict:
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}
    account.create_order()
    return account.uncompleted_order.to_dict()
    
@app.post('/order/apply_coupon/', tags=["order"])
def apply_coupon(token: str, code: str) -> dict:
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}
    coupon = controller.search_coupon_by_code(code)
    if coupon == None or coupon.is_valid() == False:
        return {"message" : "Coupon not found or not valid"}
    account.uncompleted_order.apply_coupon(coupon)
    return account.uncompleted_order.to_dict()

@app.post('/order/confirm_order/', tags=["order"])
def confirm_order(token: str, deli_or_pick: str, address: str, prefer_shop: int, pay_method: str) -> dict:
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}
    
    if controller.confirm_order(account.user.id, deli_or_pick, address, prefer_shop, pay_method) :
        return account.uncompleted_order.payment.to_dict()
    else :
        return {"message" : "Not enough stock"}

@app.post('/order/process_payment/', tags=["payment"])
def process_payment(token: str) -> dict:
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}
    controller.process_payment(account.user.id)
    return {"message" : "Paid"}

@app.get('/coupon/', tags=["coupon"])
def get_coupon_in_account(token: str) -> dict:
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}    
    return {'coupon_list' : [coupon.to_dict() for coupon in account.coupon_list]}

@app.get('/review/', tags=["review"])
def get_all_review(token:str) -> dict:
    acc = controller.search_account_by_user_id(token)
    if acc == None :
        return {"message" : "User not found"}
    
    return {
        'review_token' : acc.review_token,
        'review_list': [account.review_to_dict() for account in controller.customer_account_list]}

@app.post('/review/', tags=["review"])
def write_review(token: str, rating: int, comment: str) -> dict:
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}
    if account.review_token == 0:
        return {"message" : "No review token"}
    controller.write_review(account.user.id, rating, comment)
    return {"message" : "Review added"}

@app.get('/stock/', tags=["stock"])
def get_shops(token: str) -> dict :
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}
    if account.user.role != "shop":
        raise HTTPException(status_code=403, detail="Permission denied")
    shop = controller.search_shop_by_id(account.branch)
    return shop.shop_stock.to_dict()

@app.post('/stock/restock/', tags=["stock"])
def restock(token: str) -> dict:
    account = controller.search_account_by_user_id(token)
    if account == None :
        return {"message" : "User not found"}
    if account.user.role != "shop":
        raise HTTPException(status_code=403, detail="Permission denied")
    shop = controller.search_shop_by_id(account.branch)
    shop.restock()
    return {"message" : "Restock success"}