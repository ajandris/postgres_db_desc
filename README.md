# postgres_db_desc

This is a commandline tool for documenting postgresql database tables. The result is a md file.

GitHub: https://github.com/ajandris/postgres_db_desc

# Author
Andris Jancevskis

Date: 03/11/2024

# Additional features
* Can create a list what tables to exclude - look for TABLE_EXCLUSION_LIST in the code. Initially there is Django exclusion list
* Postgres specific column types can be replaced with more common ones - look for REPLACE_COLUMN_TYPE_NAME. 

# Known issues
1. Multiple column constraints (keys) are generated as separate constraint for each column
2. Not tested with Cloud databases/ no URL connection tested

# Software versions

Program is developed and tested on (the full Python module list is in the file requirements.txt)
* Python v3.12.2
* PostgreSQL v16
* psycopg2 v2.9.10

# Deployment

These instructions are for Windows OS.

1. Make project directory
2. Copy project files into project directory
3. Create env.py file in the project root and enter following lines and change ```<xyz>``` with requested informantion

```
import os

# Database
os.environ.setdefault("PG_DATABASE_NAME", "<database name>")
os.environ.setdefault("PG_DATABASE_USER", "<database_user>")
os.environ.setdefault("PG_DATABASE_PASSWORD", "<password>")
os.environ.setdefault("PG_DATABASE_HOST", "<database server host>")
os.environ.setdefault("PG_DATABASE_PORT", "<database server port, usually 5432>")
```

4. Create virtual environment
```
py -m venv .venv
```
5. Activate virtual environment

```
.venv\Scripts\Activate.bat
```
6. install required modules from requirements.txt
```
pip install -r requirements.txt
```
7. run the program
```
py main.py
```
The resulting file is **structure.md** in the project directory. 
