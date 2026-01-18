# dashboard.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Invoice, InvoiceItem
import os

# ---------------------
# Database configuration
# ---------------------
DATABASE_URL = "postgresql+psycopg2://invoice_user:strongpassword@localhost/shopping_invoice"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------
# Helper: Fetch invoices
# ---------------------
def fetch_invoices():
    db = SessionLocal()
    invoices_data = []
    try:
        invoices = db.query(Invoice).all()
        for inv in invoices:
            items = db.query(InvoiceItem).filter(InvoiceItem.invoice_id == inv.id).all()
            items_str = ", ".join([f"{i.name}({i.quantity}x{i.price})" for i in items])
            invoices_data.append({
                "Invoice No": inv.invoice_no,
                "Customer": inv.customer_name,
                "Phone": inv.phone,
                "Date": inv.date,
                "Subtotal": inv.subtotal,
                "CGST": inv.cgst,
                "SGST": inv.sgst,
                "Total": inv.total,
                "Items": items_str,
                "PDF": getattr(inv, "pdf_path", "")
            })
    finally:
        db.close()
    return pd.DataFrame(invoices_data)

# ---------------------
# Streamlit UI
# ---------------------
st.set_page_config(page_title="Invoice Dashboard", layout="wide")
st.title("📊 Invoice Dashboard")

# Load data
df = fetch_invoices()

if df.empty:
    st.warning("No invoices found in the database.")
else:
    # ---------------------
    # Filters
    # ---------------------
    col1, col2, col3 = st.columns(3)
    with col1:
        search_invoice = st.text_input("Search by Invoice No")
    with col2:
        search_customer = st.text_input("Search by Customer Name")
    with col3:
        search_date = st.text_input("Search by Date (YYYY-MM-DD)")

    # Apply filters
    filtered_df = df.copy()
    if search_invoice:
        filtered_df = filtered_df[filtered_df["Invoice No"].str.contains(search_invoice, case=False)]
    if search_customer:
        filtered_df = filtered_df[filtered_df["Customer"].str.contains(search_customer, case=False)]
    if search_date:
        filtered_df = filtered_df[filtered_df["Date"].str.contains(search_date, case=False)]

    # ---------------------
    # Show Table
    # ---------------------
    st.subheader("Invoices Table")
    st.dataframe(filtered_df)

    # Download CSV
    st.download_button(
        label="Download CSV",
        data=filtered_df.to_csv(index=False),
        file_name="invoices.csv",
        mime="text/csv"
    )

    # ---------------------
    # Sales Overview
    # ---------------------
    st.subheader("📈 Sales Overview")
    sales_df = filtered_df.groupby("Date")["Total"].sum().reset_index()
    st.bar_chart(sales_df.set_index("Date"))
    st.line_chart(sales_df.set_index("Date"))

    # ---------------------
    # Item-wise Sales
    # ---------------------
    st.subheader("🛒 Item-wise Sales")
    items_list = []
    for idx, row in filtered_df.iterrows():
        items = row["Items"].split(", ")
        for i in items:
            try:
                name_qty_price = i.split("(")
                name = name_qty_price[0]
                qty_price = name_qty_price[1].replace(")", "")
                qty, price = qty_price.split("x")
                items_list.append({"Item": name, "Quantity": int(qty), "Price": float(price)})
            except:
                continue
    if items_list:
        items_df = pd.DataFrame(items_list)
        item_summary = items_df.groupby("Item").sum()[["Quantity", "Price"]].reset_index()
        st.dataframe(item_summary)
        st.bar_chart(item_summary.set_index("Item")["Price"])
        st.subheader("Item Sales Distribution")
        st.pyplot(item_summary.set_index("Item")["Price"].plot.pie(autopct='%1.1f%%', figsize=(5,5)).figure)

    # ---------------------
    # Tax Analysis
    # ---------------------
    st.subheader("💰 Tax Analysis")
    tax_df = filtered_df[["CGST", "SGST"]].sum().reset_index()
    tax_df.columns = ["Tax Type", "Amount"]
    st.bar_chart(tax_df.set_index("Tax Type")["Amount"])

    # ---------------------
    # Top Customers
    # ---------------------
    st.subheader("🏆 Top Customers")
    top_customers = filtered_df.groupby("Customer")["Total"].sum().sort_values(ascending=False).reset_index()
    st.dataframe(top_customers)
    st.bar_chart(top_customers.set_index("Customer")["Total"])

    # ---------------------
    # PDF Download Links
    # ---------------------
    st.subheader("📄 Invoice PDFs")
    for idx, row in filtered_df.iterrows():
        pdf_path = row.get("PDF")
        if pdf_path and os.path.exists(pdf_path):
            st.download_button(
                label=f"Download {row['Invoice No']}",
                data=open(pdf_path, "rb").read(),
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )
        else:
            st.write(f"PDF not available for {row['Invoice No']}")
