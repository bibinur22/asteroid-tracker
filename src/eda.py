import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

con = sqlite3.connect("data/asteroids.db")
df = pd.read_sql("SELECT * FROM approaches", con, parse_dates=["approach_date"])

# 1. Сближений по месяцам
monthly = df.groupby(df.approach_date.dt.to_period("M")).size()
monthly.index = monthly.index.astype(str)
plt.figure(figsize=(12, 5))
monthly.plot(kind="bar")
plt.title("Close approaches per month")
plt.xlabel("Month")
plt.ylabel("Approaches")
plt.xticks(rotation=60)
plt.tight_layout()
plt.savefig("data/monthly.png", dpi=150)
plt.close()

# 2. Распределение размеров (логарифмическая шкала)
plt.figure(figsize=(8, 5))
plt.hist(np.log10(df.diam_max_km * 1000), bins=40)
plt.title("Asteroid size distribution")
plt.xlabel("log10(max diameter, meters)")
plt.ylabel("Approaches")
plt.tight_layout()
plt.savefig("data/sizes.png", dpi=150)
plt.close()

# 3. Размер и расстояние пролёта, опасные выделены цветом
plt.figure(figsize=(8, 6))
for flag, color, label in [(0, "tab:blue", "not hazardous"), (1, "tab:red", "hazardous")]:
    d = df[df.hazardous == flag]
    plt.scatter(d.miss_lunar, d.diam_max_km * 1000, s=6, alpha=0.5, c=color, label=label)
plt.xscale("log")
plt.yscale("log")
plt.title("Miss distance vs size")
plt.xlabel("Miss distance (lunar distances)")
plt.ylabel("Max diameter (m)")
plt.legend()
plt.tight_layout()
plt.savefig("data/size_vs_distance.png", dpi=150)
plt.close()

# Числа для README
print("approaches:", len(df))
print("unique asteroids:", df.neo_id.nunique())
print("unique hazardous asteroids:", df[df.hazardous == 1].neo_id.nunique())
print("median diameter (m):", round(df.diam_max_km.median() * 1000, 1))
print("approaches closer than the Moon:", (df.miss_lunar < 1).sum())