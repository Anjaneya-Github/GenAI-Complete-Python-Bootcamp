from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://invoice_user:strongpassword@localhost/shopping_invoice"
)

with engine.connect() as conn:
    print("✅ Database connection successful")
