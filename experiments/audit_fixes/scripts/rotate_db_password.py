"""Rotate legal_xai DB password without exposing secrets in logs.

Reads old URL from experiments/audit_fixes/replay/.db_env (gitignored),
reads new password from experiments/audit_fixes/replay/.db_new_password (gitignored),
connects with old URL, runs ALTER USER, writes new URL to .db_env.new.
Never prints secrets; only prints status and lengths.
"""
from __future__ import annotations
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, quote

import psycopg
from psycopg import sql

base = Path("experiments/audit_fixes/replay")
old_line = (base / ".db_env").read_text(encoding="ascii").strip()
assert old_line.startswith("LEGAL_XAI_DATABASE_URL="), "bad .db_env format"
old_url = old_line.split("=", 1)[1]
new_password = (base / ".db_new_password").read_text(encoding="ascii").strip()
assert len(new_password) >= 20, "new password too short"

print(f"old URL len={len(old_url)} new password len={len(new_password)}")
with psycopg.connect(old_url) as conn:
    with conn.cursor() as cur:
        cur.execute(sql.SQL("ALTER USER legal_xai WITH PASSWORD {}").format(sql.Literal(new_password)))
    conn.commit()
print("ALTER USER committed")

parts = urlsplit(old_url)
assert parts.username == "legal_xai", f"unexpected user {parts.username}"
new_netloc = f"legal_xai:{quote(new_password, safe='')}@{parts.hostname}:{parts.port}"
new_url = urlunsplit((parts.scheme, new_netloc, parts.path, parts.query, parts.fragment))
(base / ".db_env.new").write_text(f"LEGAL_XAI_DATABASE_URL={new_url}\n", encoding="ascii")
print(f"wrote .db_env.new len={len(new_url)}")

# Verify new URL works (without printing it)
with psycopg.connect(new_url) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM corpus_chunks")
        n = cur.fetchone()[0]
print(f"new URL verification: corpus_chunks count={n}")
