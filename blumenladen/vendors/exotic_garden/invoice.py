import pathlib

import camelot

from blumenladen import models

SENDER_EMAIL = "mail@exoticgarden.de"


def extract_purchases(path: pathlib.Path, date: str) -> list[models.Purchase]:
    """Extract the flowers from the PDF file."""
    tables = camelot.read_pdf(path)
    purchases = []
    for table in tables:
        for row in table.df.itertuples():
            product_id = str(row[0])
            for row in table.df.itertuples():
                n_bunches = int(row[1])
                bunch_size = int(row[2])
                price = int(
                    float(row[4].replace(" €", "").replace(",", ".")) * 100
                )
                percentage = int(row[5].replace("%", ""))
                purchases.append(
                    models.Purchase(
                        date=date,
                        product_id=product_id,
                        n_bunches=n_bunches,
                        bunch_size=bunch_size,
                        price=price,
                        percentage=percentage,
                    )
                )
    return purchases
