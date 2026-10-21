import os, requests, sqlite3, time
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["NASA_API_KEY"]
URL = "https://api.nasa.gov/neo/rest/v1/feed"

con = sqlite3.connect("data/asteroids.db")
con.execute("""
CREATE TABLE IF NOT EXISTS approaches (
    neo_id TEXT, name TEXT, approach_date TEXT,
    abs_mag REAL, diam_min_km REAL, diam_max_km REAL,
    velocity_kms REAL, miss_km REAL, miss_lunar REAL,
    hazardous INTEGER,
    PRIMARY KEY (neo_id, approach_date)
)""")

def fetch_week(start, tries=5):
    end = start + timedelta(days=6)
    for attempt in range(tries):
        try:
            r = requests.get(URL, params={
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "api_key": API_KEY}, timeout=60)
            r.raise_for_status()
            return r.json()["near_earth_objects"]
        except requests.exceptions.RequestException as e:
            print("retry", attempt + 1, "for", start, "-", type(e).__name__)
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"failed for week {start}")

row = con.execute("SELECT MAX(approach_date) FROM approaches").fetchone()[0]
start = date.fromisoformat(row) - timedelta(days=7) if row else date(2024, 1, 1)
print("starting from", start)

while start < date.today():
    for day, neos in fetch_week(start).items():
        for n in neos:
            ca = n["close_approach_data"][0]
            con.execute(
                "INSERT OR IGNORE INTO approaches VALUES (?,?,?,?,?,?,?,?,?,?)",
                (n["id"], n["name"], day, n["absolute_magnitude_h"],
                 n["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
                 n["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
                 float(ca["relative_velocity"]["kilometers_per_second"]),
                 float(ca["miss_distance"]["kilometers"]),
                 float(ca["miss_distance"]["lunar"]),
                 int(n["is_potentially_hazardous_asteroid"])))
    con.commit()
    print("loaded week from", start)
    start += timedelta(days=7)
    time.sleep(1)