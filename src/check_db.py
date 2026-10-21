import sqlite3
con = sqlite3.connect("data/asteroids.db")
print("rows:", con.execute("SELECT COUNT(*) FROM approaches").fetchone()[0])
print("dates:", con.execute("SELECT MIN(approach_date), MAX(approach_date) FROM approaches").fetchone())
print("hazardous:", con.execute("SELECT SUM(hazardous) FROM approaches").fetchone()[0])
print("closest approaches:")
for r in con.execute("SELECT name, approach_date, miss_lunar, diam_max_km FROM approaches ORDER BY miss_km LIMIT 5"):
    print(r)