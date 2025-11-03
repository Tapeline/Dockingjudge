import logging

import psycopg2

logger = logging.getLogger(__name__)

DATABASES = [
    {
        "dbname": "account_db",
        "user": "pguser",
        "password": "pgpass",
        "host": "localhost",
        "port": "5500"
    },
    {
        "dbname": "contest_db",
        "user": "pguser",
        "password": "pgpass",
        "host": "localhost",
        "port": "5501"
    },
    {
        "dbname": "solution_db",
        "user": "pguser",
        "password": "pgpass",
        "host": "localhost",
        "port": "5503"
    }
]


def purge_everything():
    for db in DATABASES:
        _purge_db(db)


def _purge_db(db_params):
    conn = None
    logger.info("Dropping data")
    try:
        conn = psycopg2.connect(**db_params)
        conn.autocommit = False
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
            """
        )
        tables = [row[0] for row in cursor.fetchall()]
        if not tables:
            return
        truncate_command = (
            f"TRUNCATE TABLE {", ".join(tables)} RESTART IDENTITY CASCADE;"
        )
        cursor.execute(truncate_command)
        conn.commit()
    except psycopg2.Error as exc:
        if conn:
            conn.rollback()
        logger.exception("Data drop error")
    finally:
        if conn:
            conn.close()
