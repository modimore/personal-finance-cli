import os, sqlite3
from breezeblocks import Database

_dsn = os.path.join(os.path.dirname(__file__), "..", "db.sqlite")

db = Database(dsn=_dsn, dbapi_module=sqlite3)
