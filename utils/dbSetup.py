from dotenv import load_dotenv
import psycopg2 
def initializeDB(user, host, database):
    conn = psycopg2.connect(
        database="aspira",
        user="postgres",
        host="localhost"
    )

    cursor = conn.cursor()

    return cursor, conn





