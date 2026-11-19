from uuid import UUID
import os
from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extensions import connection as PgConnection

from models import User

INSERT_ITEM_QUERY = "INSERT INTO users (name, age, sex) VALUES (%s, %s, %s) RETURNING user_id"
SELECT_ITEM_QUERY = "SELECT name, age, sex FROM users WHERE user_id = %s"

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")

app = FastAPI()

@app.get("/")
def landing_page():
    return {"message": "Hello, Welcome to Mac Lab!"}

@app.post("/add", status_code=201)
def add_user(user: User) -> dict:

    print("Adding the user...")
    connection = get_connection()

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_ITEM_QUERY, [user.name, user.age, user.sex])
                user_id = cursor.fetchone()[0]

        return {"user_id": user_id}

    except Exception as ex:
        print(f"Error while inserting the user in database: {ex}")
        raise

    finally:
        close_connection(connection)

@app.get("/user/{user_id}")
def get_user(user_id: UUID) -> dict:

    print("Getting the user...")
    connection = get_connection()

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_ITEM_QUERY, [str(user_id)])
                item = cursor.fetchone()

    except Exception as ex:
        print(f"Error while fetching the user from database: {ex}")
        raise

    finally:
        close_connection(connection)

    if item is None:
        raise HTTPException(status_code=404, detail="User not found")

    name, age, sex = item
    return {
        "user_id": user_id,
        "name": name,
        "age": age,
        "sex": sex
    }

def get_connection() -> PgConnection:

    print("Connecting to database...")
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )

        db_version = connection.server_version
        print(f"Successfully connected! PostgreSQL version: {db_version}")
        return connection

    except Exception as ex:
        print(f"Error connecting to database: {ex}")
        raise

def close_connection(connection: PgConnection) -> None:

    print("Closing connection to database...")
    try:
        if connection is not None:
            connection.close()
        print("Database connection closed.")

    except Exception as ex:
        print(f"Error closing database connection: {ex}")
