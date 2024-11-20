from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://tana_user:Tana123.@localhost/tana"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    print("Database connection successful!")
    connection.close()
except Exception as e:
    print(f"Database connection failed: {e}")

