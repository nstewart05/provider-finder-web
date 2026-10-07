import sqlite3

DB_PATH = "app.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY, 
            tmdb_id INTEGER NOT NULL,
            media_type TEXT NOT NULL,
            title TEXT NOT NULL,
            year TEXT,
            added_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (tmdb_id, media_type)
        )
    """)
    # PRIMARY KEY means that this value is unique and cannot be repeated
    # built in SQL function
    conn.commit()
    conn.close()

def add_to_watchlist(tmdb_id, media_type, title, year):
    conn = get_connection()
    try:
        conn.execute( #the question marks makes it so users cannot use SQL commnads from their input
            "INSERT INTO watchlist (tmdb_id, media_type, title, year) VALUES (?, ?, ?, ?)",
            (tmdb_id, media_type, title, year),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_watchlist():
    conn = get_connection() #conn will stay mostly the same through every project
    rows = conn.execute(
        "SELECT id, tmdb_id, media_type, title, year, added_at "
        "FROM watchlist ORDER BY added_at DESC, id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def remove_from_watchlist(item_id):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM watchlist WHERE id = ?", (item_id,))
    conn.commit()
    removed = cursor.rowcount > 0
    conn.close()
    return removed

if __name__ == "__main__":
    create_tables()
    print("Tables ready.")

#Bottlenecks will get created if there are too many users, this isnt a problem because this is a learning project
#Potential Soltuions for later:
#with blocks to open and close connections automatically, so you can't forget close()
#ORM such as SQLAlchemy-> lets you work with Python classes and objects instead of writing SQL strings
#Dependency injection in FastAPI, where the framework opens a connection for each request and hands it to your endpoint function, so each function doesn't open its own.