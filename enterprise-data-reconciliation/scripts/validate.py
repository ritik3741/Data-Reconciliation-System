import sqlite3
import pandas as pd

conn = sqlite3.connect("database/enterprise.db")

query = """
SELECT
    a.transaction_id,
    a.account_id,
    a.amount AS amount_a,
    b.amount AS amount_b
FROM source_a a
LEFT JOIN source_b b
ON a.transaction_id = b.transaction_id
"""

df = pd.read_sql(query, conn)

df["status"] = df.apply(
    lambda row:
    "MATCH" if row["amount_a"] == row["amount_b"]
    else "MISMATCH" if pd.notnull(row["amount_b"])
    else "MISSING_IN_B",
    axis=1
)

print(df)
conn.close()
