import logging
import os

import fastapi
import uvicorn
from fastapi.middleware import cors

from blumenladen import db, maillib, models
from blumenladen.vendors.exotic_garden import invoice as eg_invoice

logger = logging.getLogger(__name__)


app = fastapi.FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def update_flower_database() -> str:
    """Update the flower database with the latest purchases."""
    connection = db.create_connection()
    since_date = db.get_last_updated(connection)
    mail = maillib.connect_to_imap()
    email_ids = maillib.search_emails(
        mail, eg_invoice.SENDER_EMAIL, since_date
    )
    purchases = []
    for email_id in email_ids:
        if db.check_and_insert_email_id(connection, email_id):
            continue
        pdf_date, pdf_file = maillib.download_pdf_attachment(mail, email_id)
        if not pdf_file or not pdf_date:
            continue
        purchases.extend(eg_invoice.extract_purchases(pdf_file.name, pdf_date))
        pdf_file.close()

    db.insert_purchases(connection, purchases)
    return db.update_last_updated(connection)


@app.post("/version", status_code=200)
def update_flowers():
    """Return a welcome message."""
    try:
        date = update_flower_database()
        return {"success": True, "date": date}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/version", status_code=200)
def get_last_updated() -> dict:
    """Return the date of the last update."""
    connection = db.create_connection()
    last_updated = db.get_last_updated(connection)
    if not last_updated:
        try:
            last_updated = update_flower_database()
        except Exception as e:
            return {"success": False, "error": str(e)}
    return {"succsess": True, "date": last_updated}


@app.get("/flowers", status_code=200)
def list_flowers() -> list[models.Flower]:
    """Return a list of flowers with theri most recent purchase."""
    connection = db.create_connection()
    return db.get_all_flowers(connection)


@app.get("/flowers/{flower_name}", status_code=200)
def get_flower(flower_name: str) -> models.Flower:
    """Return the flower with the given name."""
    connection = db.create_connection()
    purchases = db.get_flower_purchases(connection, flower_name)
    return models.Flower(product_id=flower_name, purchases=purchases)


@app.get("/costs/{group_by}", status_code=200)
def get_costs(
    group_by: str,
    from_date: str = fastapi.Query(None, alias="from"),
    to_date: str = fastapi.Query(None, alias="to"),
) -> list[models.TotalCost]:
    """Return the costs grouped by the given column."""
    connection = db.create_connection()
    return db.get_total_cost_by_group(group_by, from_date, to_date, connection)


# @app.post("/order/start", status_code=201)
# def start_order(vendor: str, flower_ids: list[str]) -> list[models.Purchase]:
#     """Start a new order with the given flower ids."""
#     return []


def start_server():
    connection = db.create_connection()
    try:
        db.setup_database(connection)
    except Exception as e:
        logger.error("Error setting up database: %s", e)
        return
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    start_server()
