import os
import pathlib

import fastapi
import uvicorn
from fastapi import responses
from fastapi.middleware import cors

from blumenladen import db, maillib, models
from blumenladen.vendors.exotic_garden import invoice as eg_invoice

DB_PATH = pathlib.Path(
    "/home/huyenngn/Documents/blumenladen/blumenladen/test.db"
)

app = fastapi.FastAPI()

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.connection = None


def update_flower_database():
    """Update the flower database with the latest purchases."""
    since_date = db.get_last_updated(app.state.connection)
    mail = maillib.connect_to_imap()
    email_ids = maillib.search_emails(
        mail, eg_invoice.SENDER_EMAIL, since_date
    )
    purchases = []
    for email_id in email_ids:
        pdf_date, pdf_file = maillib.download_pdf_attachment(mail, email_id)
        if not pdf_file:
            continue
        purchases.extend(eg_invoice.extract_purchases(pdf_file.name, pdf_date))
        pdf_file.close()

    db.insert_purchases(app.state.connection, purchases)
    db.update_last_updated(app.state.connection)


@app.post("/update", status_code=200)
def update_flowers() -> responses.JSONResponse:
    """Return a welcome message."""
    update_flower_database()
    return responses.JSONResponse(
        status_code=200,
        content={"success": True, "message": "Database updated."},
    )


@app.get("/flowers", status_code=200)
def list_flowers() -> list[models.Flower]:
    """Return a list of flowers with theri most recent purchase."""
    return db.get_all_flowers(app.state.connection)


@app.get("/flowers/{flower_name}", status_code=200)
def get_flower(flower_name: str) -> models.Flower:
    """Return the flower with the given name."""
    purchases = db.get_flower_purchases(app.state.connection, flower_name)
    return models.Flower(product_id=flower_name, purchases=purchases)


# @app.post("/order/start", status_code=201)
# def start_order(vendor: str, flower_ids: list[str]) -> list[models.Purchase]:
#     """Start a new order with the given flower ids."""
#     return []


def start_server():
    app.state.connection = db.create_connection(DB_PATH)
    assert app.state.connection
    db.setup_database(app.state.connection)
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    start_server()
