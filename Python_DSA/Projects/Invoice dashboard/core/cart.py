class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def subtotal(self):
        return sum(item.total() for item in self.items)
