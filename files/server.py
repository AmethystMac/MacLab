from uuid import UUID
from fastapi import FastAPI
import psycopg2
from models import User

INSERT_ITEM_QUERY = "INSERT INTO users (name, age, sex) VALUES (%s, %s, %s) RETURNING user_id"
SELECT_ITEM_QUERY = "SELECT name, age, sex FROM users WHERE user_id = %s"

app = FastAPI()

@app.get("/")
def landing_page():
    return {"message": "Hello, Welcome to Mac Lab!"}

@app.post("/add")
def add_user(user: User) -> dict:

    print("Adding the user...")
    try:
        cursor, connection = connect_to_db()

        if cursor is not None:
            cursor.execute(INSERT_ITEM_QUERY, (user.name, user.age, user.sex))
            user_id = cursor.fetchone()[0]
            connection.commit()

            return (
                {
                    "response": "200",
                    "user_id": user_id
                }
            )

    except Exception as ex:
        print(f"Error while inserting the user in database: {ex}")
        connection.rollback()
        raise

    finally:
        close_db_connection(cursor, connection)

    return (
        {
            "response": "400",
            "user_id": None
        }
    )

@app.get("/user/{user_id}")
def get_user(user_id: UUID) -> dict:

    print("Getting the user...")
    try:
        cursor, connection = connect_to_db()

        if cursor is not None:
            cursor.execute(SELECT_ITEM_QUERY, (user_id))
            item = cursor.fetchone()

            if item is not None:
                name, age, sex = item
                return {
                    "response": "200",
                    "user_id": user_id,
                    "name": name,
                    "age": age,
                    "sex": sex
                }

    except Exception as ex:
        print(f"Error while fetching the user from database: {ex}")
        raise

    finally:
        close_db_connection(cursor, connection)

    return {
        "response": "400",
        "user_id": user_id,
        "name": None,
        "age": None,
        "sex": None
    }

def connect_to_db() -> None:

    print("Connecting to database...")
    try:
        connection = psycopg2.connect(
            host="db",
            database="testdb",
            user="dbuser",
            password="secure_password",
            port="5432"
        )
    
        cursor = connection.cursor()
        db_version = connection.server_version
        print(f"Successfully connected! PostgreSQL version: {db_version}")
        return cursor, connection

    except Exception as ex:
        print(f"Error connecting to database: {ex}")
        raise

def close_db_connection(cursor: any, connection: any) -> None:

    print("Closing connection to database...")
    try:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
        print("Database connection closed.")

    except Exception as ex:
        print(f"Error closing database connection: {ex}")