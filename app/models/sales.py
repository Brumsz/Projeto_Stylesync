from pydantic import BaseModel
from datetime import date
from bson import ObjectId

class Sales(BaseModel):
    sale_date:date
    product_id:str
    quantity:int
    total_value:int
    