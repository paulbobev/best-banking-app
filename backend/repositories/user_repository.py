# repositories/user_repository.py
from db import get_cursor
from models.user_entity import User


class UserRepository:

    def create(self, name: str, email: str) -> int:
        with get_cursor(commit=True) as cur:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email),
            )

            user_id = cur.lastrowid
            if user_id is None:
                raise RuntimeError("User insert did not return an ID")

            return int(user_id)

    def find_by_id(self, user_id: int) -> User | None:
        with get_cursor() as cur:
            cur.execute(
                "SELECT user_id, name, email FROM users WHERE user_id = ?",
                (user_id,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            return User(row["user_id"], row["name"], row["email"])

    def find_by_email(self, email: str) -> User | None:
        with get_cursor() as cur:
            cur.execute(
                "SELECT user_id, name, email FROM users WHERE email = ?",
                (email,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            return User(row["user_id"], row["name"], row["email"])

    def find_all(self) -> list[User]:
        with get_cursor() as cur:
            cur.execute("SELECT user_id, name, email FROM users ORDER BY user_id")
            return [User(r["user_id"], r["name"], r["email"]) for r in cur.fetchall()]
