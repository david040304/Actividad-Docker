import psycopg2
import psycopg2.extras
from flask import g, current_app


def get_db():
    """Devuelve una conexión a PostgreSQL reutilizable por request."""
    if "db" not in g:
        cfg = current_app.config
        g.db = psycopg2.connect(
            host=cfg["DB_HOST"],
            port=cfg["DB_PORT"],
            dbname=cfg["DB_NAME"],
            user=cfg["DB_USER"],
            password=cfg["DB_PASSWORD"],
        )
        g.db.autocommit = True
    return g.db


def close_db(_exc=None):
    """Cierra la conexión al terminar el request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Crea la tabla contacts si no existe al arrancar."""
    with app.app_context():
        cfg = app.config
        conn = psycopg2.connect(
            host=cfg["DB_HOST"],
            port=cfg["DB_PORT"],
            dbname=cfg["DB_NAME"],
            user=cfg["DB_USER"],
            password=cfg["DB_PASSWORD"],
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id    SERIAL PRIMARY KEY,
                    name  VARCHAR(120) NOT NULL,
                    phone VARCHAR(30)  NOT NULL,
                    email VARCHAR(120)
                );
            """)
        conn.close()
