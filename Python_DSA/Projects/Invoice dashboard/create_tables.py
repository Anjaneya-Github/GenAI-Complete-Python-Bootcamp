from sqlalchemy import create_engine, text
from database.models import Base

DATABASE_URL = "postgresql+psycopg2://invoice_user:strongpassword@localhost/shopping_invoice"

engine = create_engine(DATABASE_URL, echo=True)

with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS invoice_schema"))
    conn.commit()

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully")

