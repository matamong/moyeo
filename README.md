# **Moyeo**
What's the best time for us to get together????? <br>
Let's **Moyeo**!!! **Quickly**!!! <br>
🏃‍♀️🏃‍♀️🏃‍♀️🏃‍♀️🏃‍♀️

➡️ Moyeo's Frontend: moyeo-fe(https://github.com/matamong/moyeo-fe)

<br>

# Backend Start
```shell
uvicorn app.main:app --reload
```
⚠️ Need .env file!

<br>

# Docker Start
```shell
# Set environment var for Traefik
$ export USERNAME=admin
$ export PASSWORD=password
$ export USEREMAIL=example@example.com
$ export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)

# Create docker network
$ docker network create traefik-public

# Up the traefik container
$ docker compose -f docker-compose.traefik.yml up -d

# Up the FastAPI container
$ docker compose -f docker-compose.yml up -d

```
⚠️ Need .env file!

<br>

## Stack (So far...)
- Python 11.1
- FastAPI 0.88
- Postgresql 15

## Used
- SQLAlchemy
- Alembic
- uvicorn
