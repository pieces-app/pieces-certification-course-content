import json
import sqlite3

from flask import g

STOCK_DATABASE = "stock.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(STOCK_DATABASE)
    return db


def close_connection():
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def is_db_initialized(app):
    with app.app_context():
        db = get_db()
        cur = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='stock'"
        )
        return cur.fetchone() is not None


def init_db_if_required(app):
    if not is_db_initialized(app):
        with app.app_context():
            db = get_db()
            with app.open_resource("schema.sql", mode="r") as f:
                db.cursor().executescript(f.read())
            db.commit()
        _load_data(app)


def _load_data(app):
    with app.app_context():
        db = get_db()

        with open("stock.json", "r") as f:
            data = json.load(f)
            for entry in data:
                db.execute(
                    "INSERT INTO stock (name, image, description) VALUES (?, ?, ?)",
                    (entry["name"], entry["image"], entry["description"]),
                )

        db.commit()

class Stock:
    def __init__(self, name, image, description) -> None:
        self.name = name
        self.image = image
        self.description = description

def load_stock(app):
    with app.app_context():
        db = get_db()
        init_db_if_required(app)
        cur = db.execute("SELECT name, image, description FROM stock")

        stock = []
        for c in cur:
            stock_item = Stock(c.name, c.image, c.description)
            stock.append[stock_item]

        return stock
