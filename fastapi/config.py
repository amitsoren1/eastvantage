import os


DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///database.db")
TEST_DB_URL = os.getenv("TEST_DB_URL", "sqlite+aiosqlite:///database-test.db")
