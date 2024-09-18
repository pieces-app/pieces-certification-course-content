import json
import sqlite3

from flask import g

STOCK_DATABASE = "stock.db"

def close_connection():
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def _isDbInitialized(app):
    with app.app_context():
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(STOCK_DATABASE)
        cur = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='stock'"
        )
        return cur.fetchone() is not None

def _initDbIfRequired(app):
    if not _isDbInitialized(app):
        with app.app_context():
            db = getattr(g, "_database", None)
            if db is None:
                db = g._database = sqlite3.connect(STOCK_DATABASE)
            with app.open_resource("schema.sql", mode="r") as f:
                db.cursor().executescript(f.read())
            db.commit()
        _loadData(app)

def _loadData(app):
    with app.app_context():
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(STOCK_DATABASE)

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
        _initDbIfRequired(app)

        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(STOCK_DATABASE)
        id_cur = db.execute("SELECT id FROM stock")

        stock = []
        for id_row in id_cur.fetchall():
            cur = db.execute("SELECT name, image, description FROM stock WHERE id = ?", (id_row[0],))
            row = cur.fetchone()

            stock_item = Stock(row.name, row.image, row.description)
            stock.append(stock_item)

        return stock
