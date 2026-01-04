import sqlite3
import pandas as pd

conn = sqlite3.connect("database/enterprise.db")

df_a = pd.read_csv("data/source_a.csv")
df_b = pd.read_csv("data/source_b.csv")

df_a.to_sql("source_a", conn, if_exists="replace", index=False)
df_b.to_sql("source_b", conn, if_exists="replace", index=False)

print("Data loaded successfully")
conn.close()
