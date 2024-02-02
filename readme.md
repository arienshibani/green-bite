# Green Bite API 🌱
Green Bite __attempts__ to calculate sustainability scores for food. Sometimes it even works! 🤷‍♂️ Part of my masters thesis on ingredient matching to determine the sustainability of online recipes. (Information Science, UiB: 2020).


## How are sustainability scores calculated? 💡
Using this formula
`(amount_kg * land_usage) + (amount_kg * greenhouse_gas_emissions) = sustainability_score`

### Based on what data? 🤓

* The [SHARP database](https://www.sciencedirect.com/science/article/pii/S2352340919309722). Environmental impacts of 40,000 foods commonly eaten in 40 countries.
* Simple weight tables to convert between volumetric and mass measurements.
* **Alot** of assumptions and simplifications. Take the results with a shovel of salt. 🧂

## Quickstart
* Make sure you have [Docker](https://www.docker.com/get-started) installed and that it is running.

1. ✨ Clone repo `git clone git@github.com:arienshibani/green-bite.git`

2. 🏗️ Navigate into repo and build the image `docker build .` 

3. 🐋 Run container  `docker run -p 80:80 green-bite`

Open API specification should now be available locally! 👉 http://0.0.0.0/docs

## Example Usage

![image](https://github.com/arienshibani/green-bite/assets/22197324/2df0c8f0-e957-4385-aff2-60cc5d1afa05)


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
