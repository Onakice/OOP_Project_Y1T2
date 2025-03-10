import uuid
from user import User
from account import Account, Customer_account, Shop_account
from shop import Shop
from coupon import Coupon
from basket import Basket
from pizza import Pizza, Pizza_item
from drink import Drink, Drink_item
from payment import Payment
from order import Order
from review import Review

class Controller :
    def __init__(self) -> None:
        self.__user_list = []
        self.__customer_account_list = []
        self.__shop_account_list = []
        self.__shop_list = []
        self.__pizza_list = []
        self.__drink_list = []
        self.__coupon_list = []
        self.__review_list = []

    @property
    def user_list(self) -> list:
        return self.__user_list
    
    @property
    def customer_account_list(self) -> list:
        return self.__customer_account_list
    
    @property
    def shop_list(self) -> list:
        return self.__shop_list
    
    @property
    def pizza_list(self) -> list:
        return self.__pizza_list
    
    @property
    def drink_list(self) -> list:
        return self.__drink_list
    
    @property
    def coupon_list(self) -> list:
        return self.__coupon_list
    
    @property
    def review_list(self) -> list:
        return self.__review_list
    
    def add_customer_account(self, user_name: str, password: str) -> Customer_account:
        user = self.search_user_by_name(user_name)
        if user and user.role == "customer":
            customer_account = Customer_account(user, password)
            self.__customer_account_list.append(customer_account)
            return customer_account
        else:
            raise None
        
    def add_shop_account(self, user_name: str, password: str) -> Shop_account:
        user = self.search_user_by_name(user_name)
        if user and user.role == "shop":
            shop_account = Shop_account(user, password)
            self.__shop_account_list.append(shop_account)
            return shop_account
        else:
            return None

    def add_user(self, name: str, role: str, password: str) -> None:
        self.__user_list.append(User(name, role))
        if role == "customer":
            self.add_customer_account(name, password)
        elif role == "shop":
            self.add_shop_account(name, password)

    def add_shop(self, shop_id_branch: int) -> Shop:
        shop = Shop(shop_id_branch)
        if isinstance(shop, Shop) :
            self.__shop_list.append(shop)
            return shop
        else:
            raise None

    def show_user_list(self) -> list:
        return self.__user_list
    
    def show_account_list(self) -> list:
        return self.__customer_account_list + self.__shop_account_list
    
    def search_user_by_id(self, user_id: str) -> User:
        for user in self.user_list:
            if user.id == user_id:
                return user
        return None

    def search_user_by_name(self, name: str) -> User:
        for user in self.user_list:
            if user.name == name:
                return user
        raise None
    
    def search_account_by_name(self, name: str) -> Account:
        for account in self.__customer_account_list + self.__shop_account_list:
            if account.user.name == name:
                return account
        return None
    
    def search_account_by_user_id(self, user_id: str) -> Account:
        for account in self.__customer_account_list + self.__shop_account_list:
            if account.user.id == user_id:
                return account
        return None
    
    def get_user_id_by_name(self, name: str) -> str:
        for user in self.user_list:
            if user.name == name:
                return user.id
        return None
    
    def search_shop_by_id(self, shop_id_branch: int) -> Shop:
        for shop in self.__shop_list:
            if shop.shop_id_branch == shop_id_branch:
                return shop
        return None
    
    def check_stock(self, shop_id_branch: int) -> list:
        for shop in self.shop_list:
            if shop.shop_id_branch == shop_id_branch:
                return shop.shop_stock
        return None
            
    def add_stock_to_shop(self, shop_id_branch: int, stock_items: list) -> None:
        for shop in self.__shop_list:
            if shop.shop_id_branch == shop_id_branch:
                shop.add_stock(stock_items)    
            return None
    
    def add_pizza(self, name: str, price: int) -> Pizza:
        pizza = Pizza(name, price)
        self.__pizza_list.append(pizza)
        return pizza
    
    def add_drink(self, name: str, price: int) -> Drink:
        drink = Drink(name, price)
        self.__drink_list.append(drink)
        return drink
    
    def get_pizza(self, face: str) -> Pizza:
        for pizza in self.__pizza_list:
            if pizza.face == face:
                return pizza
        raise None
    
    def get_drink(self, name: str) -> Drink:
        for drink in self.__drink_list:
            if drink.name == name:
                return drink
        raise None
    
    
    def create_pizza_item(self, face: str , size: str, quantity: int) -> Pizza_item:
        pizza = self.get_pizza(face)
        return Pizza_item(pizza, size, quantity)
    
    def create_drink_item(self, name: str, size: str, quantity: int) -> Drink_item:
        drink = self.get_drink(name)
        return Drink_item(drink, size, quantity)
    
    def search_order_by_id(self, order_id: str) -> Order:
        for account in self.__customer_account_list:
            for order in account.completed_order_list:
                if order.id == order_id:
                    return order
        return None
    
    def confirm_order(self, user_id: str,deli_or_pick: str, address: str, prefer_shop: int, pay_method: str) -> None:
        account = self.search_account_by_user_id(user_id)
        account.add_address(address)
        account.add_prefer_shop(prefer_shop)
        account.uncompleted_order.set_address(address)
        account.uncompleted_order.set_prefer_shop(prefer_shop)
        account.uncompleted_order.set_deli_or_pick(deli_or_pick)

        pizza_amount = len(account.uncompleted_order.basket.pizza_list)
        drink_amount = len(account.uncompleted_order.basket.drink_list)
        
        shop = self.search_shop_by_id(prefer_shop)
        pizza_in_stock = shop.shop_stock.pizza_amount
        drink_in_stock = shop.shop_stock.drink_amount

        if pizza_amount > pizza_in_stock or drink_amount > drink_in_stock:
            return False
        
        shop.shop_stock.set_pizza_amount(pizza_in_stock - pizza_amount)
        shop.shop_stock.set_drink_amount(drink_in_stock - drink_amount)

        account.uncompleted_order.create_payment(pay_method)
        return True
    
    def process_payment(self, user_id: str):
        account = self.search_account_by_user_id(user_id)
        account.add_order(account.uncompleted_order)
        account.add_review_token(1)
        account.uncompleted_order.payment.process_payment()

        account.clear_basket()
        account.clear_uncompleted_order()

    def add_coupon(self, coupon: Coupon) -> None:
        self.__coupon_list.append(coupon)

    def remove_coupon(self, coupon: Coupon) -> None:
        self.__coupon_list.remove(coupon)
    
    def search_coupon_by_code(self, code: str) -> Coupon:
        for coupon in self.__coupon_list:
            if coupon.code == code:
                return coupon
        raise None
    
    def add_coupon_to_account(self, user_id: str, coupon_code: str) -> None:
        account = self.search_account_by_user_id(user_id)
        coupon = self.search_coupon_by_code(coupon_code)
        account.add_coupon(coupon)

    def write_review(self, user_id: str, rating: int, comment: str ) -> None:
        account = self.search_account_by_user_id(user_id)
        if account and account.review_token > 0:
            account.add_review_token(-1)
            review = Review(rating, comment)
            account.add_review(review)
        else:
            return None

    def get_all_review(self) -> list:
        reviews = []
        for account in self.__customer_account_list:
            if account.review_list:
                for review in account.review_list:
                    reviews.append(review)