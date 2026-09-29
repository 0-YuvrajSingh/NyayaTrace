"""Verify current .db_env URL works (no secrets printed)."""
import os
import psycopg

url = os.environ["LEGAL_XAI_DATABASE_URL"]
print(f"URL len={len(url)}")
with psycopg.connect(url) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM corpus_chunks")
        print("new_URL_OK count=", cur.fetchone()[0])
