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

    # Django internal tables. Create another one for your app
    TABLE_EXCLUSION_LIST = ['django_admin_log', 'django_content_type', 'django_migrations', 'django_session', 'auth_user_user_permissions',
                            'auth_user_groups', 'auth_user', 'auth_permission', 'auth_group_permissions', 'auth_group']
    
    # Uncomment to get all tables
    #TABLE_EXCLUSION_LIST = []

    # replace internal representation of column types to more user friendly
    REPLACE_COLUMN_TYPE_NAME = {
        'timestamp with time zone': 'datetime',
        'character varying': 'varchar'
    }

    # uncomment to leave original column types
    #REPLACE_COLUMN_TYPE_NAME = dict()


    conn = get_connection()

    file = open(file_name, "w")


    #
    # Table
    #
    cursor = conn.cursor()
    sql = "select tab.table_name, ds.description \
    	from information_schema.tables tab \
            left join pg_catalog.pg_class cl on (tab.table_name = cl.relname) \
            left join pg_catalog.pg_description ds on (cl.oid = ds.objoid and ds.objsubid = 0) \
    	where table_schema = 'public'"
    cursor.execute(sql)

    for row in cursor.fetchall():
        #
        # Column
        #
        if row[0] in TABLE_EXCLUSION_LIST:
            continue

        table_name = row[0]
        file.write(f"\n\n## Table: {table_name}\n")
        if row[1] is not None:
            file.write(f"Table description: {row[1]}\n")


        # Primary Key
        pk_cur = conn.cursor()
        sql = f"select kku.constraint_name, kku.column_name, kku.table_name \
                from \
                    information_schema.key_column_usage kku, \
                    information_schema.table_constraints tc \
                where \
                    kku.table_schema = 'public' \
                    and kku.constraint_name = tc.constraint_name \
                    and tc.constraint_type = 'PRIMARY KEY' \
                    and tc.table_name = '{table_name}'"
        pk_cur.execute(sql)

        file.write("\n### Primary Key: \n")
        for pk in pk_cur.fetchall():
            file.write(f'"{pk[0]}" on column "{pk[1]}"\n\n')

        pk_cur.close()


        # Primary Key
        uk_cur = conn.cursor()
        sql = f"select kku.constraint_name, kku.column_name, kku.table_name \
                from \
                    information_schema.key_column_usage kku, \
                    information_schema.table_constraints tc \
                where \
                    kku.table_schema = 'public' \
                    and kku.constraint_name = tc.constraint_name \
                    and tc.constraint_type = 'UNIQUE' \
                    and tc.table_name = '{table_name}'"
        uk_cur.execute(sql)

        if uk_cur.rowcount > 0 :
            file.write("\n### Unique Key: \n")
            for uk in uk_cur.fetchall():
                file.write(f'"{uk[0]}" on column "{uk[1]}"\n\n')

        uk_cur.close()


        # Foreign Keys
        file.write("### Foreign Key(s): \n\n")
        fk_cur = conn.cursor()
        sql = f"SELECT constraint_name, unique_constraint_name as refering_to \
            FROM information_schema.referential_constraints where constraint_name like '{table_name}_%'"
        
        fk_cur.execute(sql)
        for fk in fk_cur.fetchall():
             file.write(f"Name: {fk[0]}, refering to \n\n")       

        pk_cur.close()

        # Columns
        cur_col = conn.cursor()
        sql = f"select col.column_name, col.data_type, col.character_maximum_length, col.is_identity, col.ordinal_position, ds.description \
        	from information_schema.columns col \
		        left join pg_catalog.pg_class cl on (col.table_name = cl.relname) \
		        left join pg_catalog.pg_description ds on (cl.oid = ds.objoid and col.ordinal_position = ds.objsubid) \
            where table_schema = 'public' and table_name = '{row[0]}' order by ordinal_position"

        cur_col.execute(sql)

        file.write("### Columns\n")

        file.write(f"| |Column Name|Data Type|Key|Description|\n")
        file.write("|---|---|---|---|---|\n")

        for col_row in cur_col.fetchall():
            col_id = col_row[4]
            col_name = col_row[0]
            description = col_row[5] if col_row[5] is not None else ''
            col_data_type = col_row[1]
            if col_data_type in REPLACE_COLUMN_TYPE_NAME.keys():
                col_data_type = REPLACE_COLUMN_TYPE_NAME[col_data_type]

            if col_row[2] is not None:
                col_data_type += f"({col_row[2]})"
 
            col_is_key = f"{col_row[3]}" if col_row[3] == 'YES' else ''

            file.write(f"|{col_id}|{col_name}|{col_data_type} |{col_is_key}|{description}|\n")

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
