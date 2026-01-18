class Item:
    def __init__(self, name, price, quantity, unit):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.unit = unit

    def total(self):
        return self.price * self.quantity
