# postgres_db_desc

This commandline tool describes postgresql database structure and creates md file to be copied into a project README.md file. 


# Deployment

1. Create env.py file in the project root and enter following lines and change ```<xyz>``` with requested informantion

```
import os

# Database
os.environ.setdefault("PG_DATABASE_NAME", "<database name>")
os.environ.setdefault("PG_DATABASE_USER", "<database_user>")
os.environ.setdefault("PG_DATABASE_PASSWORD", "<password>")
os.environ.setdefault("PG_DATABASE_HOST", "<database server host>")
os.environ.setdefault("PG_DATABASE_PORT", "<database server port, usually 5432>")
```

2. Create virtual environment
```
python3 -m venv .venv
```
3. Activate virtual environment
```
For windows:
.venv\Scripts\Activate.bat
```
4. install required modules from requirements.txt
```
pip install -r requirements.txt
```
5. run the program
```
python3 main.py
```
The resulting file is **structure.md** in the project root folder. 
