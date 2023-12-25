# Green Bite API 🌱
Green Bite is an API that __attempts__ to utilize regular expressions, NLP and public data to calculate sustainability scores for food. Sometimes it even works! 🤷‍♂️ 

## How is it calculated? 💡
`(amount * land_usage) + (amount * greenhouse_gas_emissions) = sustainability_score`

### Based on what data? 🤓

* The [SHARP database](https://www.sciencedirect.com/science/article/pii/S2352340919309722). Environmental impacts of 40,000 foods commonly eaten in 40 countries.
* Simple weight tables to convert between volumetric and mass measurements.

### What's the catch? 🤨
The API makes __a lot__ of assumptions and simplifications. Take the results with a grain of salt. 🧂

* __GHGE__ and __Land usage__ are the only metrics used, and they are weighted equally.
* False positives are to be expected. The RegEx / NLP used to find matches is very basic.
  * Use the `/parse` endpoint to inspect the details and make your own judgement.
* Many ingredients are not in the database (or not in the format one might expect them to be).


## Quickstart

1. Clone the repo

2. Build everything 👉 `docker build -t green-bite`

3. Spin it up 👉 `docker run -p 80:80 green-bite`

The API should now be available locally! 👉 http://0.0.0.0/docs
