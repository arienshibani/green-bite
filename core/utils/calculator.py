import pandas as pd
import warnings
from core.utils.measurement_conversions import convert_measurement_to_kg
from core.utils.ingredient_parser import get_ingredient_description, get_quantity, get_unit_of_measurement

# Mute irrelevant pandas warnings
warnings.filterwarnings('ignore', category=UserWarning)


# Filepath to CSV data
sharp_csv = 'core/data/SHARP.csv'
frequencies_csv = 'core/data/ingredient_frequency.csv'
weight_table_csv = 'core/data/weight_table.csv'


sharp = pd.read_csv(sharp_csv,
                    usecols=[
                        "Food item", "GHGE of 1 kg food as consumed_kgCO2eq",
                        "Land use of 1 kg food as consumed_m2_yr"
                    ])

# Apply .map() to each column (Series) in the DataFrame
for column in sharp.select_dtypes(include=['object']).columns:  # select columns with strings
    sharp[column] = sharp[column].map(lambda s: s.lower() if isinstance(s, str) else s)

sharp = sharp.rename(columns={"GHGE of 1 kg food as consumed_kgCO2eq": 'GHGE',
                              "Land use of 1 kg food as consumed_m2_yr": 'Land Use'})
food_weights = pd.read_csv(weight_table_csv)
frequencies = pd.read_csv(frequencies_csv)
frequencies = frequencies.sort_values('frequency', ascending=False)


def lookup_weight_in_grams(parsed_ingredient_description: str = "egg") -> int:
    # Utility function for finding the weight of one whole unit of an ingredient:
    try:
        # See if any entry in the 'ingredients' column conatins the parameter - parsed_ingredient_description
        search_result_weights = food_weights[food_weights['ingredient'].str.contains(
            parsed_ingredient_description
        )]
        search_result_weights = search_result_weights.reset_index()
        item_weight = int(search_result_weights.at[0, 'grams'])
        return item_weight
    except KeyError:
        return 0
    except ValueError:
        return 0


'''
Ingredientmatcher.py

This file handles the retrieval of GHGE and LU data from the SHARP dataset. By matching the parsed raw ingredient descriptions from "ingredientparser.py" and using them as a parameter in match_ingredient().
'''


def match_ingredient(ingredient_description: str, use_frequencies: bool = True) -> pd.DataFrame:
    '''
    Performs a regex.search() on all Food Item names in the SHARP-DB, and returns a dataframe with potential matches. The first match is used by default.
    '''
    search_result_sharp = None
    ingredient_description = ingredient_description.lower()

    # Performing a str.match() first, and check wether or not there are results could be usefull.

    try:
        # Filter the sharp dataframe to only contain possible matches (using regular expressions)
        search_result_sharp = sharp[sharp['Food item'].str.contains(
            ingredient_description)]

        if len(search_result_sharp) == 1:
            return search_result_sharp.reset_index()

        if (use_frequencies):
            '''
            For each ingredient in the now regex-filtered SHARP dataset (a subset of potential ingredient matches),
            we pick the one which has has the highest ingredient_frequency in ingredient_frequencies.csv.

            (frequencies here simply mean how often that ingredient has occured in all the recipes.)
            '''
            filtered_indexed_sharp = search_result_sharp.reset_index()

            most_frequent_ingredient = None
            most_frequent_ingredient_df = pd.DataFrame(
                {'index': [0], 'Food item': [0], 'GHGE': [0], 'Land Use': [0]})

            # For each ingredient in the filtered SHARP dataset:
            for i in range(0, len(filtered_indexed_sharp)):
                food_items_rank = 0  # Get the ingedient's name
                food_item = filtered_indexed_sharp.at[i, 'Food item']
                food_items_ghge = filtered_indexed_sharp.at[i, 'GHGE']
                food_items_LU = filtered_indexed_sharp.at[i, 'Land Use']

                frequencies_search_result = frequencies[frequencies['ingredient_name'].str.contains(
                    food_item, regex=False)]  # Use that name as a parameter, to filter the frequencies dataset

                frequencies_search_result = frequencies_search_result.reset_index()

                # If there's a match in the frequency dataset:
                if len(frequencies_search_result) > 0:
                    # Retrieve that ingredients frequency
                    food_items_rank = frequencies_search_result.at[0, 'frequency']

                # If this is the first ingredient we compute the frequency for:
                if most_frequent_ingredient is None:
                    most_frequent_ingredient = (
                        str(food_item), int(food_items_rank))
                    most_frequent_ingredient_df = pd.DataFrame(
                        {'index': [0], 'Food item': [food_item], 'GHGE': [food_items_ghge], 'Land Use': [food_items_LU]})

                # Otherwise, overwrite the previous ingredient, only if the current's frequency is higher
                elif most_frequent_ingredient[1] < food_items_rank:

                    most_frequent_ingredient = (
                        str(food_item), int(food_items_rank))
                    most_frequent_ingredient_df = pd.DataFrame(
                        {'index': [0], 'Food item': [food_item], 'GHGE': [food_items_ghge], 'Land Use': [food_items_LU]})

            return most_frequent_ingredient_df

    except KeyError:
        print("Something went wrong when filtering out the SHARP dataset for potential ingredient matches.", KeyError)
        return sharp

    except Exception:
        return sharp

    return search_result_sharp.reset_index()


def calculate_score(raw_ingredient_string: str) -> float:
    '''
    Calculates the sustainability score of an ingredient string (i.e: "2 ounces of milk")
    Performs a re.search() based filter with it on the SHARP database. Calculates the availables scores found and returns the sustainability score.

    '''

    def add_sustainability_factors(amount: int, ghge: float, land_usage: float) -> float:
        '''Amount has to be in kilograms.'''
        return (amount * land_usage) + (amount * ghge)

    score = 0

    ingredient = get_ingredient_description(raw_ingredient_string)
    search = match_ingredient(ingredient)

    # If there's a match between recipe ingredient and SHARP-DB:
    if len(search) > 0:
        # Retrieve the sustainability properties.
        ghge = float(search.at[0, 'GHGE'])
        land_use = float(search.at[0, 'Land Use'])

        quantity = get_quantity(raw_ingredient_string)
        measurement = get_unit_of_measurement(raw_ingredient_string)

        if measurement == 'whole':
            # If the measurement used is provided as 'whole' we try to find the ingredients weight in the weight_table.csv
            measurement = 'grams'
            # Returns 0 if weight not found
            quantity = (lookup_weight_in_grams() * quantity)

        quantity_kg = convert_measurement_to_kg(measurement, quantity)

        try:
            score = add_sustainability_factors(quantity_kg, ghge, land_use)
        except TypeError:
            return score

    return score


def get_food_match(raw_ingredient_string: str) -> float:
    '''
    Returns the food item that was used as a match.
    '''

    ingredient = get_ingredient_description(raw_ingredient_string)
    search = match_ingredient(ingredient)

    print(search)

    return search.at[0, 'Food item']
