# Green Bite API 🌱

![Test Status](https://github.com/arienshibani/green-bite/actions/workflows/run-tests.yml/badge.svg) 

API for parsing ingredient strings and calculating the environmental impact of the parsed food item. 

* `"2 pounds smoked salmon" 👉 9.724508593539`
*  `"10 cups of shallots (diced)" 👉 1.649056635080645`
*  `"¼ cup fresh lemon juice" 👉 0.10300892338709677`
  


![301833855-2df0c8f0-e957-4385-aff2-60cc5d1afa05 (1)](https://github.com/user-attachments/assets/52077c6b-4fa7-475b-be08-0cc18453711d)

## How are sustainability scores calculated? 💡

Using this formula
`(amount_kg * land_usage) + (amount_kg * greenhouse_gas_emissions) = sustainability_score`

### Based on what data? 🤔

* The [SHARP database](https://www.sciencedirect.com/science/article/pii/S2352340919309722). Environmental impacts of 40,000 foods commonly eaten in 40 countries.
* Simple weight tables to convert between volumetric and mass measurements.
* __A lot__ of assumptions and simplifications. Take the results with a pinch of salt. 🧂

### Ingredient strings 🥕

The API uses __ingredient strings__ to produce scores. A string of characters that consist of three key elements: a __name__, an __amount__ and the __unit__ used to specify that amount. Every recipe contains a set of them. For example: `1 kilogram of beef` or `cheese, 2 pounds (Parmesan)` are both instances of an ingredient string.

## Try it out 🚀

- You can test the API and generate scores for ingredients via the [interactive API documentation](https://green-bite-production.up.railway.app/docs)

## Run Locally  ⚙️

* Make sure you have [Docker](https://www.docker.com/get-started) installed and that it is running.

1. ✨ Clone repo `git clone git@github.com:arienshibani/green-bite.git`

2. 🏗️ Navigate into repo and build the image `docker build -t green-bite .`

3. 🐋 Run container  `docker run -p 80:80 green-bite`

The Open API specification should now be available locally via your webbrowser 👉 <http://0.0.0.0/docs>, and you can test the API.

## API Usage 📚

The API exposes two main endpoints. One for parsing individual ingredient strings and one for scoring entire recipes.

### `GET /parse/ingredient/{ingredientString}`

The __parse/ingredient__ endpoint takes an __ingredient string__ as input and returns a sustainability score along with details about the ingredient. The details can be useful for debugging and understanding which entry was actually used to produce the score.

* The string must be sent in as a query parameter.
  * Example request URL for calculating the score of 1kg Bacon 👉 `/parse/ingredient/1%20kg%20of%20bacon`

```jsonc
{ // Successful 200 Response.
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

### `POST /score?ingredients=1%{ingredientString#1}%2{ingredientString#2}`

 The __score__ endpoint can be used to score any number of ingredient strings. Given an array of ingredient strings, it returns the combined sustainability score. Only the score is returned, no details about the individual ingredients. This endpoint is particularly useful for scoring entire recipes.

* The array of ingredient strings must be sent in as query parameters.
* Example request URL for calculating a simple milk pudding recipe containing milk, sugar and cornstarch. 👇
  * `http://0.0.0.0/score?ingredients=1%20cups%20of%20milk&ingredients=3%20tablespoons%20sugar&ingredients=2%20tablespoons%20cornstarch`

```jsonc
// Successful 200 response
0.7855314915881078
```

## Local Development 🛠️

* Make sure you have [Python 3.9 or above](https://www.python.org/downloads/) and `makefile` installed (makefile should already be installed if you are on a linux or a mac).

1. ✨ Clone repo `git clone git@github.com:arienshibani/green-bite.git`

2. 🏗️ Navigate into repo and run `make install`

3. ⚙️ Start the API `make start`

## Disclaimers 📜

* This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license.
  * Feel free to use, share and adapt this software for any non-commercial purposes. Credit is appreciated.
* This software was developed solely for academic purposes as part of my master's thesis: _"Ingredient matching to determine the sustainability of online recipes (Information Science, UiB: 2022)"_.
* The data used to calculate the scores is based on the SHARP database and is not my own. I take no responsibility for the accuracy of the data or the results produced by this software.
