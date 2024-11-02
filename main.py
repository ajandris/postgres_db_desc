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

    # Setting constants

    # Django internal tables. Create a new one for your app
    TABLE_EXCLUSION_LIST = ['django_admin_log', 'django_content_type', 'django_migrations', 'django_session', 'auth_user_user_permissions',
                            'auth_user_groups', 'auth_user', 'auth_permission', 'auth_group_permissions', 'auth_group']

    # replace internal representation of column types to more user friendly
    REPLACE_COLUMN_TYPE_NAME = {
        'timestamp with time zone': 'datetime',
        'character varying': 'varchar'
    }


    conn = get_connection()

    file = open(file_name, "w")


    #
    # Table
    #
    cursor = conn.cursor()
    sql = "select table_name from information_schema.tables where table_schema = 'public' order by table_name"
    cursor.execute(sql)

    for row in cursor.fetchall():
        #
        # Column
        #
        if row[0] in TABLE_EXCLUSION_LIST:
            continue

        file.write(f"## Table: {row[0]}\n")

        cur_col = conn.cursor()
        sql = f"select column_name, data_type, character_maximum_length, is_identity, ordinal_position \
                from information_schema.columns \
                    where table_schema = 'public' and table_name = '{row[0]}' order by ordinal_position"

        cur_col.execute(sql)

        file.write("### Columns\n")

        file.write(f"| |Column Name|Data Type|Key|\n")
        file.write("|---|---|---|---|\n")

        for col_row in cur_col.fetchall():
            col_id = col_row[4]
            col_name = col_row[0]

            col_data_type = col_row[1]
            if col_data_type in REPLACE_COLUMN_TYPE_NAME.keys():
                col_data_type = REPLACE_COLUMN_TYPE_NAME[col_data_type]

            if col_row[2] is not None:
                col_data_type += f"({col_row[2]})"
 
            col_is_key = f"{col_row[3]}" if col_row[3] == 'YES' else ''

            file.write(f"|{col_id}|{col_name}|{col_data_type} |{col_is_key}|\n")

        cur_col.close()


    file.close()
    cursor.close()
    conn.close()

#
# Application starting point
#
if __name__ == '__main__':
    OUTPUT_FILE_NAME = 'structure.md'
    main(file_name = OUTPUT_FILE_NAME)
