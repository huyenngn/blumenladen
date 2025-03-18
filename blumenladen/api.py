import logging
import os

import dotenv
import fastapi
import uvicorn
from fastapi.middleware import cors

from blumenladen import db, maillib, models
from blumenladen.vendors.exotic_garden import invoice as eg_invoice

dotenv.load_dotenv()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")

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

app.state.is_updating = False


def update_flower_database() -> str:
    """Update the flower database with the latest purchases."""
    logger.debug("Updating with %s", os.environ.get("EMAIL_ACCOUNT"))
    if app.state.is_updating:
        raise Exception("Already updating")
    try:
        app.state.is_updating = True
        connection = db.create_connection()
        logger.debug("Connected to database")
        since_date = db.get_last_updated(connection)
        logger.debug("Last updated: %s", since_date)
        mail = maillib.connect_to_imap()
        logger.debug("Connected to IMAP")
        email_ids = maillib.search_emails(
            mail, eg_invoice.SENDER_EMAIL, since_date
        )
        logger.debug("Found %d new emails", len(email_ids))
        files_to_delete = []
        for email_id in email_ids:
            if db.email_id_exists(connection, email_id):
                continue
            pdf_date, pdf_path = maillib.download_pdf_attachment(
                mail, email_id
            )
            if not pdf_path or not pdf_date:
                continue
            logger.debug("Downloaded PDF from %s", pdf_date)
            purchases = eg_invoice.extract_purchases(pdf_path, pdf_date)
            logger.debug("Extracted %d purchases", len(purchases))
            db.insert_purchases(connection, purchases)
            logger.info(
                "Inserted %d purchases from %s", len(purchases), pdf_date
            )
            files_to_delete.append(pdf_path)
            db.insert_email_id(connection, email_id)
            logger.debug("Inserted email id %s", email_id)

        for file_path in files_to_delete:
            os.remove(file_path)
        db.update_last_updated(connection)
    finally:
        app.state.is_updating = False

    res = db.get_last_updated(connection)
    logger.debug("Returning last updated date: %s", res)
    assert res
    return res


@app.post("/version", status_code=200)
def update_flowers():
    """Return a welcome message."""
    try:
        date = update_flower_database()
        return {"success": True, "date": date}
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e)) from e


@app.get("/version", status_code=200)
def get_last_updated() -> dict:
    """Return the date of the last update."""
    connection = db.create_connection()
    last_updated = db.get_last_updated(connection)
    if not last_updated:
        raise fastapi.HTTPException(
            status_code=404, detail="No data available"
        )
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
    logger.debug(
        "Getting costs for %s from %s to %s", group_by, from_date, to_date
    )
    return db.get_total_cost_by_group(group_by, from_date, to_date, connection)


def start_dev_server():
    start_server(debug=True)


def start_server(debug: bool = False):
    log_level = "debug" if debug else "info"
    connection = db.create_connection()
    try:
        db.setup_database(connection)
    except Exception as e:
        logger.error("Error setting up database: %s", e)
        return
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(
        "blumenladen.api:app",
        host="0.0.0.0",
        port=port,
        log_level=log_level,
        reload=debug,
    )


if __name__ == "__main__":
    start_dev_server()
