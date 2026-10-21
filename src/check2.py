import sqlite3
con = sqlite3.connect("data/asteroids.db")

print("rows:", con.execute("SELECT COUNT(*) FROM approaches").fetchone()[0])
print("unique asteroids:", con.execute("SELECT COUNT(DISTINCT neo_id) FROM approaches").fetchone()[0])

print("most frequent asteroids:")
for r in con.execute("""SELECT name, COUNT(*) AS c FROM approaches
                        GROUP BY neo_id ORDER BY c DESC LIMIT 5"""):
    print(r)