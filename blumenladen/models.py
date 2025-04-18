import pydantic


class Purchase(pydantic.BaseModel):
    date: str
    product_id: str
    n_bunches: int
    bunch_size: int
    price: int
    percentage: int


class Flower(pydantic.BaseModel):
    product_id: str
    purchases: list[Purchase]


class TotalCost(pydantic.BaseModel):
    group_by: str
    cost: int


class DateResponse(pydantic.BaseModel):
    date: str
