from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

SCHEMA = "invoice_schema"


class Invoice(Base):
    __tablename__ = "invoices"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True)
    invoice_no = Column(String, unique=True, nullable=False)
    customer_name = Column(String)
    phone = Column(String)
    date = Column(String)
    subtotal = Column(Float)
    cgst = Column(Float)
    sgst = Column(Float)
    total = Column(Float)

    items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True)

    # 🚨 THIS IS THE CRITICAL LINE 🚨
    invoice_id = Column(
        Integer,
        ForeignKey("invoice_schema.invoices.id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    total = Column(Float)

    invoice = relationship("Invoice", back_populates="items")
