import logging
import pathlib
import sqlite3
from datetime import datetime

from blumenladen import models

logger = logging.getLogger(__name__)


def create_connection(path: pathlib.Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    logger.info("Connection to SQLite DB successful")

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


def _execute_read_query(
    connection: sqlite3.Connection, query: str
) -> tuple[sqlite3.Cursor, list]:
    cursor = connection.cursor()
    rows = []
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        logger.error("The error '%s' occurred", e)
    return cursor, rows


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


def update_last_updated(connection: sqlite3.Connection) -> str:
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
    return today


def purchase_factory(cursor: sqlite3.Cursor, row: list) -> models.Purchase:
    fields = [col[0] for col in cursor.description]
    return models.Purchase(**dict(zip(fields, row, strict=True)))


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
    cursor, rows = _execute_read_query(connection, query)
    flowers = []
    for row in rows:
        flower = models.Flower(
            product_id=row[1],
            purchases=[purchase_factory(cursor, row)],
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
    ORDER BY date DESC
    """
    cursor, rows = _execute_read_query(connection, query)
    purchases = []
    for row in rows:
        purchases.append(purchase_factory(cursor, row))
    return purchases


def total_cost_factory(cursor: sqlite3.Cursor, row: list) -> models.TotalCost:
    fields = [col[0] for col in cursor.description]
    return models.TotalCost(**dict(zip(fields, row, strict=True)))


def get_total_cost_by_group(
    group: str, start_date: str, end_date: str, connection: sqlite3.Connection
) -> list[models.TotalCost]:
    if group == "month":
        query = f"""
        SELECT strftime('%Y-%m', date) as group, SUM(n_bunches * bunch_size * price) AS cost
        FROM purchases
        WHERE date BETWEEN "{start_date}" AND "{end_date}"
        GROUP BY strftime('%Y-%m', date)
        ORDER BY group
        """
    elif group == "day":
        query = f"""
        SELECT date as group, SUM(n_bunches * bunch_size * price) AS cost
        FROM purchases
        WHERE date BETWEEN "{start_date}" AND "{end_date}"
        GROUP BY date
        ORDER BY date
        """
    elif group == "flower":
        query = f"""
        SELECT product_id as group, SUM(n_bunches * bunch_size * price) AS cost
        FROM purchases
        WHERE date BETWEEN "{start_date}" AND "{end_date}"
        GROUP BY product_id
        """
    else:
        raise ValueError(f"Invalid group: {group}")
    cursor, rows = _execute_read_query(connection, query)
    return [total_cost_factory(cursor, row) for row in rows]
