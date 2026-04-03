from pydantic import BaseModel

class PriceData(BaseModel):
    symbol: str
    price: float
    change_percent: float
    timestamp: int