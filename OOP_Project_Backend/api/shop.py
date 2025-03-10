class Shop:
    def __init__(self, shop_id_branch: int) -> None:
        self.__shop_name = 'name'
        self.__shop_id_branch = shop_id_branch
        self.__shop_stock = Shop_stock()
    
    @property
    def shop_name(self):
        return self.__shop_name
    
    @property
    def shop_id_branch(self):
        return self.__shop_id_branch
    
    @property
    def shop_stock(self):
        return self.__shop_stock
    
    def reduce_pizza_stock(self, quantity: int) -> None:
        self.__shop_stock.__pizza_amount -= quantity
    
    def reduce_drink_stock(self, quantity: int) -> None:
        self.__shop_stock.__drink_amount -= quantity
    
    def add_pizza_stock(self, quantity: int) -> None:
        self.__shop_stock.__pizza_amount += quantity

    def add_drink_stock(self, quantity: int) -> None:
        self.__shop_stock.__drink_amount += quantity

    def restock(self) -> None:
        self.__shop_stock.set_pizza_amount(Shop_stock.dialy_stock)
        self.__shop_stock.set_drink_amount(Shop_stock.dialy_stock)

class Shop_stock():
    dialy_stock = 10
    def __init__(self):
        self.__pizza_amount = self.dialy_stock
        self.__drink_amount = self.dialy_stock

    @property
    def pizza_amount(self):
        return self.__pizza_amount
    
    @property
    def drink_amount(self):
        return self.__drink_amount
    
    def set_pizza_amount(self, amount: int) -> None:
        self.__pizza_amount = amount
    
    def set_drink_amount(self, amount: int) -> None:
        self.__drink_amount = amount
    
    def to_dict(self) -> dict:
        return {'pizza_amount': self.__pizza_amount,
                'drink_amount': self.__drink_amount}