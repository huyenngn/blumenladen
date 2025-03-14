import pydantic


class Purchase(pydantic.BaseModel):
    date: str  # DD-MMM-YYYY
    product_id: str
    n_bunches: int
    bunch_size: int
    price: int  # in cents
    percentage: int  # in percent


class Flower(pydantic.BaseModel):
    product_id: str
    purchases: list[Purchase]
