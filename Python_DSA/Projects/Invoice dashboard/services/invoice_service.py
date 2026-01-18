import uuid
from database.models import Invoice, InvoiceItem
from core.invoice_calc import InvoiceCalculator

def create_invoice(db, customer, phone, cart):
    invoice_no = f"INV-{uuid.uuid4().hex[:6].upper()}"

    calc = InvoiceCalculator(cart)
    subtotal, cgst, sgst, total = calc.compute()

    invoice = Invoice(
        invoice_no=invoice_no,
        customer_name=customer,
        phone=phone,
        date="2026-01-18",
        subtotal=subtotal,
        cgst=cgst,
        sgst=sgst,
        total=total
    )

    for item in cart.items:
        invoice.items.append(
            InvoiceItem(
                name=item.name,
                price=item.price,
                quantity=item.quantity,
                unit=item.unit,
                total=item.total()
            )
        )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice
