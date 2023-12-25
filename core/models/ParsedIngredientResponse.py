from pydantic import BaseModel

class Details(BaseModel):
    quantity: float
    measurement: str
    description: str

class ParsedIngredientResponse(BaseModel):
    inputIngredientString: str = "1 kg of bacon"
    ingredientMatched: str = "bacon"
    sustainabilityScore: float = 26.05213129
    details: Details = {
        "quantity": 1.0,
        "measurement": "kg",
        "description": "bacon"
    }
