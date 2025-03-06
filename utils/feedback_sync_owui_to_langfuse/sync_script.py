import asyncio
import asyncpg
from langfuse import Langfuse
import json
import os

langfuse = Langfuse(
  secret_key=os.environ.get('LANGFUSE_PRIVATE_KEY', None),
  public_key=os.environ.get('LANGFUSE_PUBLIC_KEY', None),
  host=os.environ.get('LANGFUSE_BASE_URL', None)
)

DB_URL = os.environ.get('DB_URL', None)
INTERVAL_IN_MINS = int(os.environ.get('INTERVAL_IN_MINS', 10))

async def langfuse_ratings_action(id, data):
    langfuse_comment = {
        "reason": data.get("reason", ""),
        "comment": data.get("comment", ""),
    }
    langfuse_value = data.get("rating", 0)
    langfuse.score(
        trace_id=id,
        name="user_feedback",
        value=langfuse_value,
        comment= json.dumps(langfuse_comment),
    )

async def fetch_recent_feedback(mins=10):
    conn = await asyncpg.connect(DB_URL)
    rows = await conn.fetch(f"""
        SELECT * FROM feedback
        WHERE updated_at >= (extract(epoch from now()) - {mins * 60})::int8
    """)
    await conn.close()
    return rows
    
async def main():
    try:
        if INTERVAL_IN_MINS < 1:
            raise ValueError
    except ValueError:
        print(f"INTERVAL_IN_MINS must be a valid integer greater than 0, got {INTERVAL_IN_MINS}")
        os.exit(1)
    rows = await fetch_recent_feedback(mins=INTERVAL_IN_MINS)
    async def process_rows(rows):
        rowsDict = [dict(row) for row in rows]
        for row in rowsDict:
            data = json.loads(row.get('data')) if row.get('data') else row.get('data')
            meta = json.loads(row.get('meta')) if row.get('meta') else row.get('meta')
            if data and meta:
                id = meta.get('message_id')
                await langfuse_ratings_action(id, data)
    await process_rows(rows)

asyncio.run(main())