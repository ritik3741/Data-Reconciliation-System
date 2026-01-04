import sqlite3
import pandas as pd

conn = sqlite3.connect("database/enterprise.db")

query = """
SELECT
    COALESCE(a.transaction_id, b.transaction_id) AS transaction_id,
    a.amount AS source_a_amount,
    b.amount AS source_b_amount,
    CASE
        WHEN a.transaction_id IS NULL THEN 'MISSING_IN_A'
        WHEN b.transaction_id IS NULL THEN 'MISSING_IN_B'
        WHEN a.amount != b.amount THEN 'AMOUNT_MISMATCH'
        ELSE 'MATCH'
    END AS reconciliation_status
FROM source_a a
FULL OUTER JOIN source_b b
ON a.transaction_id = b.transaction_id
"""

# SQLite workaround
df_a = pd.read_sql("SELECT * FROM source_a", conn)
df_b = pd.read_sql("SELECT * FROM source_b", conn)

result = df_a.merge(df_b, on="transaction_id", how="outer", suffixes=("_a", "_b"))

result["reconciliation_status"] = result.apply(
    lambda row:
    "MISSING_IN_A" if pd.isnull(row["amount_a"])
    else "MISSING_IN_B" if pd.isnull(row["amount_b"])
    else "AMOUNT_MISMATCH" if row["amount_a"] != row["amount_b"]
    else "MATCH",
    axis=1
)

result.to_csv("reports/reconciliation_report.csv", index=False)
print("Reconciliation report generated")

conn.close()
