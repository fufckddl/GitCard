"""
Database initialization script.

Creates database tables if they don't exist.
Run this script once to set up the database schema.

Usage:
    python init_db.py
"""
from app.database import init_db
# Import models to ensure they are registered with Base
from app.auth import db_models  # noqa: F401
from app.profiles import db_models  # noqa: F401

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")


