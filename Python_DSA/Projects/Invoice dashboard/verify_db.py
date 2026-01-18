import sqlite3

conn = sqlite3.connect("database/invoice.db")
cursor = conn.cursor()

print("\nInvoices:")
cursor.execute("SELECT * FROM invoices")
for row in cursor.fetchall():
    print(row)

print("\nInvoice Items:")
cursor.execute("SELECT * FROM invoice_items")
for row in cursor.fetchall():
    print(row)

conn.close()
