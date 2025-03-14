import logging
import pathlib
import sqlite3
from datetime import datetime

from blumenladen import models

logger = logging.getLogger(__name__)


def create_connection(path: pathlib.Path) -> sqlite3.Connection | None:
    connection = None
    try:
        connection = sqlite3.connect(path)
        logger.info("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        logger.error("The error '%s' occurred", e)

    return connection


def _execute_query(
    connection: sqlite3.Connection, query: str
) -> sqlite3.Cursor:
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logger.info("Query executed successfully")
    except sqlite3.Error as e:
        logger.error("The error '%s' occurred", e)
    return cursor


def _execute_read_query(connection: sqlite3.Connection, query: str) -> list:
    cursor = connection.cursor()
    rows = []
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        logger.error("The error '%s' occurred", e)
    return rows


def setup_database(connection: sqlite3.Connection) -> None:
    create_purchases_table = """
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        product_id TEXT NOT NULL,
        n_bunches INTEGER NOT NULL,
        bunch_size INTEGER NOT NULL,
        price INTEGER NOT NULL,
        percentage INTEGER NOT NULL
    );
    """

    create_last_updated_table = """
    CREATE TABLE IF NOT EXISTS last_updated (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL
    );
    """

    _execute_query(connection, create_purchases_table)
    _execute_query(connection, create_last_updated_table)


def insert_purchases(
    connection: sqlite3.Connection, purchases: list[models.Purchase]
) -> None:
    purchases_querys = []
    for purchase in purchases:
        purchases_querys.append(
            f'("{purchase.date}", "{purchase.product_id}", {purchase.n_bunches}, {purchase.bunch_size}, {purchase.price}, {purchase.percentage})'
        )

    query = f"""
    INSERT INTO purchases (date, product_id, n_bunches, bunch_size, price, percentage)
    VALUES {", ".join(purchases_querys)};
    """
    _execute_query(connection, query)


def get_last_updated(connection: sqlite3.Connection) -> str | None:
    query = """
    SELECT date FROM last_updated;
    """
    cursor = _execute_query(connection, query)
    row = cursor.fetchone()
    if row:
        return row[0]
    return None


def update_last_updated(connection: sqlite3.Connection) -> None:
    today = datetime.now().date().strftime("%Y-%m-%d")
    if not get_last_updated(connection):
        query = f"""
        INSERT INTO last_updated (date) VALUES ("{today}");
        """
    else:
        query = f"""
        UPDATE last_updated SET date = "{today}";
        """
    _execute_query(connection, query)


def get_all_flowers(connection: sqlite3.Connection) -> list[models.Flower]:
    """Return all flowers with only their most recent purchase."""
    query = """
    SELECT p.date, p.product_id, p.n_bunches, p.bunch_size, p.price, p.percentage
    FROM purchases p
    JOIN (
        SELECT product_id, MAX(date) AS max_date
        FROM purchases
        GROUP BY product_id
    ) latest ON p.product_id = latest.product_id AND p.date = latest.max_date
    """
    rows = _execute_read_query(connection, query)
    flowers = []
    for row in rows:
        flower = models.Flower(
            product_id=row[1],
            purchases=[
                models.Purchase(
                    date=row[0],
                    product_id=row[1],
                    n_bunches=row[2],
                    bunch_size=row[3],
                    price=row[4],
                    percentage=row[5],
                )
            ],
        )
        flowers.append(flower)
    return flowers


def get_flower_purchases(
    connection: sqlite3.Connection, flower_id: str
) -> list[models.Purchase]:
    query = f"""
    SELECT date, product_id, n_bunches, bunch_size, price, percentage
    FROM purchases
    WHERE product_id = "{flower_id}"
    """
    rows = _execute_read_query(connection, query)
    purchases = []
    for row in rows:
        purchases.append(
            models.Purchase(
                date=row[0],
                product_id=row[1],
                n_bunches=row[2],
                bunch_size=row[3],
                price=row[4],
                percentage=row[5],
            )
        )
    return purchases
