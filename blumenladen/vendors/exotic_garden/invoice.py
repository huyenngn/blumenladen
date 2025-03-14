import decimal
import re

import fitz

from blumenladen import models

SENDER_EMAIL = "mail@exoticgarden.de"

CATEGORY_PATTERN = r"\n(Grün|Schnittblumen|Pfandhandel)\n"
PRODUCT_PATTERN = r"(\S+.*?)\n(-?\d+)\n(-?\d+)\n-?\d+\n(-?\d+[,.]\d+)\s*€\n(-?\d+)\s*%\n-?\d+[,.]\d+\s*€"
CATEGORY_POLICY = {"Grün": True, "Schnittblumen": True, "Pfandhandel": False}


def extract_purchases(path: str, date: str) -> list[models.Purchase]:
    """Extract the flowers from the PDF file."""
    doc = fitz.open(path)
    purchases = []
    isProduct = False

    text = ("\n").join([page.get_text("text") for page in doc])
    category_sections = re.split(CATEGORY_PATTERN, text)

    for section in category_sections:
        policy = CATEGORY_POLICY.get(section)
        if policy is not None and policy:
            isProduct = True
            continue
        if policy is not None and not policy:
            isProduct = False
            continue
        if not isProduct:
            continue

        matches = re.finditer(PRODUCT_PATTERN, section)

        for match in matches:
            try:
                product_id = str(match.group(1))
                n_bunches = int(match.group(2))
                bunch_size = int(match.group(3))
                price = int(
                    decimal.Decimal(match.group(4).replace(",", ".")) * 100
                )
                percentage = int(match.group(5))

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
            except ValueError:
                continue

    doc.close()
    return purchases


if __name__ == "__main__":
    path = "/home/huyenngn/Documents/blumenladen/blumenladen/rg_292168.pdf"
    purchases = extract_purchases(path, "2021-01-01")
    print(purchases)
