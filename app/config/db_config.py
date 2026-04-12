import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="ep-rough-art-ai5fxyd5-pooler.c-4.us-east-1.aws.neon.tech",
        port="5432",
        user="neondb_owner",
        password="npg_PpWHj3tNrJ7b",
        dbname="neondb"
    )