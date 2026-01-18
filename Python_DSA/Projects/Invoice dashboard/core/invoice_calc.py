CGST_RATE = 0.09
SGST_RATE = 0.09

class InvoiceCalculator:
    def __init__(self, cart):
        self.cart = cart

    def compute(self):
        subtotal = self.cart.subtotal()
        cgst = subtotal * CGST_RATE
        sgst = subtotal * SGST_RATE
        total = subtotal + cgst + sgst
        return subtotal, cgst, sgst, total
