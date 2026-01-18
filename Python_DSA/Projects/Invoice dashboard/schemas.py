from pydantic import BaseModel
from typing import List


class InvoiceItemRequest(BaseModel):
    name: str
    quantity: int
    price: float
    total: float


class InvoiceRequest(BaseModel):
    invoice_no: str
    customer_name: str
    phone: str
    date: str
    subtotal: float
    cgst: float
    sgst: float
    total: float
    items: List[InvoiceItemRequest]
