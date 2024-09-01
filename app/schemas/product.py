from pydantic import BaseModel, ConfigDict


class ProductSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    name: str
    price: float
    quantity: int
