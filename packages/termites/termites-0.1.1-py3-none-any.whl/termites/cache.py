import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime

CACHE_DB_PATH = Path.home() / ".termites" / "cache.db"

def setup_cache_db():
    """Initialize SQLite cache database."""
    CACHE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(CACHE_DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                prompt_hash TEXT PRIMARY KEY,
                prompt TEXT,
                response TEXT,
                model TEXT,
                timestamp DATETIME
            )
        """)

def get_cached_response(prompt: str, model: str) -> str | None:
    """Retrieve response from cache if it exists."""
    prompt_hash = hashlib.sha256(f"{prompt}:{model}".encode()).hexdigest()
    
    with sqlite3.connect(CACHE_DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT response FROM responses WHERE prompt_hash = ?",
            (prompt_hash,)
        )
        result = cursor.fetchone()
        return result[0] if result else None

def cache_response(prompt: str, response: str, model: str) -> None:
    """Store response in cache."""
    prompt_hash = hashlib.sha256(f"{prompt}:{model}".encode()).hexdigest()
    
    with sqlite3.connect(CACHE_DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO responses 
            (prompt_hash, prompt, response, model, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (prompt_hash, prompt, response, model, datetime.now().isoformat())
        )

def get_cached_response_weave(prompt: str, model: str) -> str | None:
    import weave

    response = get_cached_response(prompt, model)
    if response is None:
        return None
    
    @weave.op()
    def get_tracked_cached_response(prompt: str, model: str) -> str | None:
        return response
    
    return get_tracked_cached_response(prompt, model)
