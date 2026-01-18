import os
from fpdf import FPDF

class PDFService:
    @staticmethod
    def generate(invoice: dict):

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # 🔥 REMOVE EMOJIS / NON-LATIN TEXT
        pdf.cell(0, 10, f"Invoice No: {invoice['invoice_no']}", ln=True)
        pdf.cell(0, 10, f"Customer: {invoice['customer_name']}", ln=True)
        pdf.cell(0, 10, f"Phone: {invoice['phone']}", ln=True)

        pdf.ln(5)
        pdf.cell(0, 10, "Items:", ln=True)

        for item in invoice["items"]:
            pdf.cell(
                0,
                8,
                f"{item['name']} | Qty: {item['qty']} | Total: {item['total']}",
                ln=True,
            )

        pdf.ln(5)
        pdf.cell(0, 10, f"Total Amount: {invoice['total']}", ln=True)

        if not os.path.exists("invoices"):
            os.makedirs("invoices")

        file_path = f"invoices/{invoice['invoice_no']}.pdf"
        pdf.output(file_path)

        return file_path
