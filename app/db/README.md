# Use Alembic! :anchor:
Moyeo use **Alembic** for database migrations. <br>
This is how to migrate tables using Alembic. Let's get it on !!!

## 1. Create Model
- In `app/models`, create(or update, delete) models that inherits from the `base` class using SQLAlchemy.
```python
# app/models/matamong.py
from app.db.base_class import Base

class Matamong(Base):
    id = ...
    awesomeness = ...

```


## 2. Create Revision File
- Create alembic's revision file so that tell alembic to track changes!
- (We use `autogenerate` for easy generating.)
```commandline
alembic revision --autogenerate -m "Initialize user entity"
```

## 3. Apply To DB
- Apply these changes to the database!
```commandline
alembic upgrade head
alembic -x dbname=test upgrade head <- For test DB
```
*`-x dbname={name}` Connect the db matching the name. Set it up in `env.py`.*

* You have to create database before use this command.*

<br><br>


# Tip
## How To Check PostgreSQL
- Connect database_name
```commandline
\connect <database_name>
```
<br>

- Check tables in database
```commandline
\d
```

<br>

- Check the fields in a table
```commandline
\d <table_name>
```

<br>

## How to reset Alembic?
1. Undo all of our changes to our database by running command below.
 ```commandline
alembic downgrade base
```
2. Remove the `alembic_version` table.
   - Located in alembic schema(In the same database).
3. Remove the alembic version files.

If the process in step 1 is not executed due to an error, <br>
try in the order of step2-3-1.


<br>

[refer article](https://medium.com/@peytonrunyan/alembic-101-897f322c9334)

<br>

## How to downgrade Alembic?
### Downgrade to last version.
```commandline
alembic downgrade -1
```

<br>

### Downgrade to specific version
1. View history
```commandline
alembic history 
```

2. Name the specific migration.
```commandline
alembic downgrade <migration-number>
```

<br>

# Errors

## When `upgrade head` after `downgrade base`, relation already exists
- Delete All the exist table and retry `upgrade head`