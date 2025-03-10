from basket import Basket
from payment import Payment
from coupon import Coupon
import time
import uuid

class Order:
    def __init__(self, basket: Basket, address, shop_id: str):
        self.__id = str(uuid.uuid4())
        self.__basket = basket
        self.__payment = None
        self.__coupon = None
        self.__deli_or_pick: str = None
        self.__address = address
        self.__perfer_shop = shop_id
        self.__time = time.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self) -> uuid:
        return self.__id

    @property
    def basket(self) -> Basket:
        return self.__basket
    
    @property
    def payment(self) -> Payment:
        return self.__payment
    
    @property
    def coupon(self) -> Coupon:
        return self.__coupon
    
    @property
    def deli_or_pick(self) -> str:
        return self.__deli_or_pick
    
    @property
    def address(self) -> str:
        return self.__address
    
    @property
    def perfer_shop(self) -> str:
        return self.__perfer_shop
    
    @property
    def time(self) -> str:
        return self.__time

    def apply_coupon(self, coupon: Coupon) -> None:
        self.__coupon = coupon
    
    def remove_coupon(self) -> None:
        self.__coupon = None

    def get_net_price(self) -> int:
        total_price = self.__basket.get_total_price()
        if self.__coupon:
            if self.coupon.is_valid():
                total_price -= self.__coupon.discount
                if total_price < 0:
                    total_price = 0
        return total_price

    def create_payment(self, payment_method:str) -> None:
        self.__payment = Payment(self.get_net_price(), payment_method)

    def set_deli_or_pick(self, method: str) -> None:
        self.__deli_or_pick = method

    def set_address(self, address: str) -> None:
        self.__address = address

    def set_prefer_shop(self, shop_id: str) -> None:
        self.__perfer_shop = shop_id

    def get_payment_status(self) -> str:
        return self.__payment.status
    
    def to_dict(self):
        return {
            "order_id": self.__id,
            "basket": self.__basket.to_dict(),
            "coupon": self.__coupon.code if self.__coupon else None,
            "price": self.get_net_price(),
            "deli_or_pick": self.__deli_or_pick,
            "address": self.__address,
            "perfer_shop": self.__perfer_shop,
            "time": self.__time
        }

