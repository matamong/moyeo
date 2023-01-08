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
```


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