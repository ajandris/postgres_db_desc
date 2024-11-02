import psycopg2
import os

# importing default environment variables (security feature)
try:
    import env
except ImportError:
    pass

#
# Opens connection to a database
#
def get_connection():
    db_name = os.getenv("PG_DATABASE_NAME")
    db_user = os.getenv("PG_DATABASE_USER")
    pwd = os.getenv("PG_DATABASE_PASSWORD")
    hostname = os.getenv("PG_DATABASE_HOST")
    db_port = int(os.getenv("PG_DATABASE_PORT"))

    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=pwd, host=hostname, port=db_port)
        return connection
    except Exception as e:
        print("Error connecting database.\nMessage: ", e)


def main(file_name):
    conn = get_connection()

    cursor = conn.cursor()
    sql = "select table_name from information_schema.tables where table_schema = 'public' order by table_name"
    cursor.execute(sql)

    for row in cursor.fetchall():
        print(row[0])


    conn.close

#
# Application starting point
#
if __name__ == '__main__':
    OUTPUT_FILE_NAME = 'structure.md'
    main(file_name = OUTPUT_FILE_NAME)
