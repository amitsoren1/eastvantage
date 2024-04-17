import os


DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///db.sqlite3")
TEST_DB_URL = os.getenv("TEST_DB_URL", "sqlite+aiosqlite:///test-db.sqlite3")
