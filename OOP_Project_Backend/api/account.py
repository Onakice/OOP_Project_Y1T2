
from basket import Basket
from order import Order
from user import User
from coupon import Coupon
from review import Review

class Account :
    def __init__ (self, user: User, password: str) -> None:
        self.__user = user
        self.__password = password
    
    @property
    def user(self) -> User:
        return self.__user
    
    @property
    def password(self) -> str:
        return self.__password
    
class Customer_account(Account):
    def __init__(self, user: User, password: str) -> None:
        super().__init__(user, password)
        self.__basket = Basket()
        self.__address = ''
        self.__prefer_shop = None
        self.__uncompleted_order = None
        self.__completed_order_list = []
        self.__coupon_list = []
        self.__review_list = []
        self.__review_token = 0

    @property
    def basket(self) -> Basket:
        return self.__basket
    
    @property
    def address(self) -> str:
        return self.__address
    
    @property
    def uncompleted_order(self) -> Order:
        return self.__uncompleted_order
     
    @property
    def completed_order_list(self) -> list:
        return self.__completed_order_list
    
    @property
    def coupon_list(self) -> list:
        return self.__coupon_list
    
    @property
    def review_token(self) -> int:
        return self.__review_token
    
    def add_address(self, address: str) -> None:
        self.__address = address

    def add_prefer_shop(self, shop_id: str) -> None:
        self.__prefer_shop = shop_id
    
    def add_coupon(self, coupon: str) -> None:
        self.__coupon_list.append(coupon)

    def remove_coupon(self, coupon: str) -> None:
        self.__coupon_list.remove(coupon)

    def create_order(self) -> None:
        self.__uncompleted_order = Order(self.__basket, self.__address, self.__prefer_shop)

    def add_order(self, order: Order) -> None:
        self.__completed_order_list.append(order)

    def clear_basket(self) -> None:
        self.__basket = Basket()

    def clear_uncompleted_order(self) -> None:
        self.__uncompleted_order = None
    
    def add_review_token(self, amount: int) -> None:
        self.__review_token += amount

    def add_review(self, review: Review) -> None:
        self.__review_list.append(review)

    def review_to_dict(self) -> list:
        return [{'user_id': self.user.name, 
                 'rating': review.rating, 
                 'comment': review.comment,
                 'time': review.time} 
                 for review in self.__review_list]

class Shop_account(Account) :
    def __init__(self, user: User, password: str) -> None:
        super().__init__(user, password)
        self.__branch = None
    
    @property
    def branch(self) -> list:
        return self.__branch
    
    def set_branch(self, shop_id: int) -> None:
        self.__branch = shop_id






