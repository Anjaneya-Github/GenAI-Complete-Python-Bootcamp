from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Invoice, InvoiceItem
from schemas import InvoiceRequest
from services.pdf_service import PDFService

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Invoice API is running!"}

@app.post("/create-invoice/")
def create_invoice(payload: InvoiceRequest, db: Session = Depends(get_db)):

    invoice = Invoice(
        invoice_no=payload.invoice_no,
        customer_name=payload.customer_name,
        phone=payload.phone,
        date=payload.date,
        subtotal=payload.subtotal,
        cgst=payload.cgst,
        sgst=payload.sgst,
        total=payload.total,
    )

    db.add(invoice)
    db.flush()  # ensures invoice.id exists

    for item in payload.items:
        db.add(
            InvoiceItem(
                invoice_id=invoice.id,
                name=item.name,
                quantity=item.quantity,
                price=item.price,
                total=item.total,
            )
        )

    db.commit()

    # Convert ORM → dict BEFORE leaving session
    invoice_data = {
        "invoice_no": invoice.invoice_no,
        "customer_name": invoice.customer_name,
        "phone": invoice.phone,
        "date": invoice.date,
        "subtotal": invoice.subtotal,
        "cgst": invoice.cgst,
        "sgst": invoice.sgst,
        "total": invoice.total,
        "items": [
            {
                "name": i.name,
                "qty": i.quantity,
                "price": i.price,
                "total": i.total,
            }
            for i in db.query(InvoiceItem)
            .filter(InvoiceItem.invoice_id == invoice.id)
            .all()
        ],
    }

    pdf_path = PDFService.generate(invoice_data)

    return {
        "status": "success",
        "invoice_no": invoice.invoice_no,
        "pdf_path": pdf_path,
    }
