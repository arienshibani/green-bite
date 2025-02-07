from fastapi import FastAPI, HTTPException, Query, Path, Body
from core.utils.calculator import calculate_score, get_food_match
from core.utils.ingredient_parser import get_parsed_string
from core.models.ParsedIngredientResponse import ParsedIngredientResponse
from typing import List


description = """
Green Bite is an API that __attempts__ to calculate sustainability scores for food. Sometimes it even works! 🤷‍♂️

## How is it calculated? 💡
`(amount * land_usage) + (amount * greenhouse_gas_emissions) = sustainability_score`

## Based on what data? 🤓

* The [SHARP database](https://www.sciencedirect.com/science/article/pii/S2352340919309722). Environmental impacts of 40,000 foods commonly eaten in 40 countries.
* Simple weight tables to convert between volumetric and mass measurements.

## What's the catch? 🤨
The API makes __a lot__ of assumptions and simplifications. Take the results with a grain of salt.

* GHGE and Land usage are the only metrics used, and they are weighted equally.
* False positives are to be expected. The RegEx / NLP used to find matches is very basic.
  * Use the `/parse` endpoint to inspect the details and make your own judgement.
* Many ingredients are not in the database (or not in the format one might expect them to be).
"""

app = FastAPI(
    title="Green Bite API 🥗",
    description=description,
    version="0.0.1",
)

@app.get("/parse/ingredient/{string}", tags=["Parse Ingredient String 🪄"])
async def parse_ingredient_string(
    string: str = Path(description="i.e: '1 kg of bacon' or '2 pounds smoked salmon'")) -> ParsedIngredientResponse:
    """
        Parse a raw ingredient string and return details about the attempted sustainability score.

    """
    parsed = parseOneIngredient(string)
    return parsed


@app.post("/score", tags=["Scoring 🌱"])

async def score(ingredients: List[str] = Query(examples=["1 pound of cheese", "2 cups of milk"])) -> float:
    """
    Calculate the combined sustainability score of 1 or more ingredients.
    """
    score = 0
    for ingredient in ingredients:
        score += calculate_score(ingredient)
    return score

def parseOneIngredient(string):
    score = calculate_score(string)
    food_match = get_food_match(string)
    details = get_parsed_string(string)

    if score is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Parses an ingredient, and returns details about DB match and sustainability score.
    res = {
        "inputIngredientString": string,
        "ingredientMatched": food_match,
        "sustainabilityScore": score,
        "details": details
        }

    return res
