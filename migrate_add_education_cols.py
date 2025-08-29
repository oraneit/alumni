import sqlite3, os
db_path = os.path.join(os.path.dirname(__file__), "orane.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

def has_col(table, name):
    cur.execute(f"PRAGMA table_info({table})")
    return any(r[1] == name for r in cur.fetchall())

adds = [
    ("alumni", "start_ym TEXT"),            # YYYY-MM
    ("alumni", "end_ym TEXT"),              # YYYY-MM
    ("alumni", "enrollment_id TEXT"),
    ("alumni", "certificate_path TEXT")
]

for table, coldef in adds:
    colname = coldef.split()[0]
    if not has_col(table, colname):
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {coldef}")
        print(f"Added {table}.{colname}")

conn.commit()
conn.close()
print("Migration complete.")
