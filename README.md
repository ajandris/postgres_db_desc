# postgres_db_desc

This commandline tool describes postgresql database structure and creates md file to be copied into a project README.md file. 


# Deployment

Create env.py file in the project root and enter following lines and change <xyz> with requested informantion

```
import os

# Database
os.environ.setdefault("PG_DATABASE_NAME", "<database name>")
os.environ.setdefault("PG_DATABASE_USER", "<database_user>")
os.environ.setdefault("PG_DATABASE_PASSWORD", "<password>")
os.environ.setdefault("PG_DATABASE_HOST", "<database server host>")
os.environ.setdefault("PG_DATABASE_PORT", "<database server port, usually 5432>")
```
