from sqlalchemy import create_engine, exc
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the database URL
SQLALCHEMY_DATABASE_URL = "postgresql://vifrtrry:psAJrlVPwhmVpQu1MY7zo77dlLqp1Xor@bubble.db.elephantsql.com/vifrtrry"

# Create the SQLAlchemy engine
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
except exc.ArgumentError:
    raise Exception("Invalid database URL. Please provide a valid database URL.")

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Additional configurations or settings can be added below if needed
