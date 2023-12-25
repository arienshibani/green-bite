# Green Bite API 🌱
Green Bite __attempts__ to calculate sustainability scores for food. Sometimes it even works! 🤷‍♂️ Part of my masters thesis on ingredient matching to determine the sustainability of online recipes. (Information Science, UiB: 2020).

## How are sustainability scores calculated? 💡
Using this formula
`(amount_kg * land_usage) + (amount_kg * greenhouse_gas_emissions) = sustainability_score`

### Based on what data? 🤓

* The [SHARP database](https://www.sciencedirect.com/science/article/pii/S2352340919309722). Environmental impacts of 40,000 foods commonly eaten in 40 countries.
* Simple weight tables to convert between volumetric and mass measurements.
* Alot of other assumptions and simplifications. Take the results with a shovel of salt. 🧂

## Quickstart

1. `git clone git@github.com:arienshibani/green-bite.git`

2. 🏗️ Build image `docker build -t green-bite` 

3. 🐋 Run container  `docker run -p 80:80 green-bite`

The API should now be available 👉 http://0.0.0.0/docs

## Example Usage

GET `http://0.0.0.0/parse/ingredient/1%20kg%20of%20bacon`

Response 👇

```json
{
 "inputIngredientString": "1 kg of bacon",
 "ingredientMatched": "bacon",
 "sustainabilityScore": 26.05213129,
 "details": {
  "quantity": 1,
  "measurement": "kg",
  "description": "bacon"
  }
}
```
