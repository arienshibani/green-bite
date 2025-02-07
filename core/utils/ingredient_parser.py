from fractions import Fraction
from textblob import TextBlob
import unicodedata
import re

'''
ingredientparser.py

Handles the parsing of raw ingredient strings.

For instance, the ingredient string: "1½ cup parmesan cheese"
would return the following using the functions defined here:

|- OUTPUT:
|-- Quantity: 1.5
|-- Measurement: Cup
|-- Ingredient Description: Parmesan Cheese

'''


def generate_list_of_all_units() -> list:
    '''Returns a list of all measurement units that our API should recognize.'''
    units = {
        'cup': {'desc': 'cup'},
        'tablespoon': {'desc': 'tbsp'},
        'teaspoon': {'desc': 'tsp'},
        'ounce': {'desc': 'ounce'},
        'gram': {'desc': 'gram'},
        'pound': {'desc': 'pound'},
        'kilogram': {'desc': 'kg'},
        'deciliter': {'desc': 'dl'},
        'milliliter': {'desc': 'ml'}
    }

    # Create a list of all measurement units that we wish to look for in a recipe string.
    list_of_units = list(set([x for key, value in units.items()
                              for x in [key, value['desc'], key + 's', value['desc'] + 's']]))
    list_of_units.sort()  # Sets are unordered, so we order them..
    # ..then reverse the list to enforce plurals being matched before singular measurements with RegEx.
    list_of_units.reverse()

    return list_of_units


list_of_units = generate_list_of_all_units()


def get_ingredient_description(raw_string: str = '100½ cups cheese', unit_exclusion_list: list = list_of_units) -> str:
    '''Retrieve the possible descriptions of an ingredient from a raw ingredient string, return them all as a tuple.

    This function attempts to remove the amount, as well as the measurement used to specify that amount, from
    a raw ingredient string from an online recipe. This (hopefully) leaves the string with the ingredient description.
    RegularExpressions are used to match unwanted parts of the raw string until the description remains.

    '''

    # Remove these words from raw ingredient strings (usually adjectives), they don't really tell you anything about the ingredient itself (other than how to prepeare it).
    blacklisted_words = ['cubed', 'package', 'vermicelli', 'halves', 'breast', 'boneless', 'skinless', 'semisweet', 'prepared', 'graham', 'ripe', 'container', 'cooked', 'package', 'packaged', 'can', 'cans',
                         'ground', 'shredded', 'crushed', 'slices', 'sliced', 'firm', 'trimmed', 'thinly', 'diced', 'medium', 'bulk', 'fluid', 'cut', 'boiling', 'french', 'italian', 'Filippo', 'Berio', "/", "-" 'bag']

    def get_noun(string: str) -> str:
        '''Returns the first noun detected in a string.
        Using TextBlob: https://textblob.readthedocs.io/en/dev/
        '''
        blob = TextBlob(string)
        for word, pos in blob.tags:
            if "NN" in pos:  # NN == Nouns
                return word
        return string

    # Substitute all occurrences of unicode fractions from the string with an empty string.
    string = re.sub(r'[\u00BC-\u00BE\u2150-\u215E\u2189]+', '', raw_string)
    # Remove parenthesis, and everything in between them
    string = re.sub(r"\([^()]*\)", "", string)
    # Substitute all occurrences of 1-9 from the string with an empty string.
    string = re.sub(r'[0-9]+', '', string)
    # Substitute all occurrences of elements found in "list_of_units" from the string with an empty string.
    string = re.sub('|'.join(unit_exclusion_list), '', string)
    # Remove blacklisted words (non food words that can be interpreted as nouns by TextBlob)
    string = re.sub('|'.join(blacklisted_words), '', string)
    # Remove commas from the string
    string = re.sub(',', '', string)

    string = get_noun(string)

    return string.strip()


def get_quantity(raw_string: str = '100 ½ cups cheese') -> str:
    '''Retrieve the specified amount of an ingredient string.

    The raw_string will be matched against two regex patterns, searching for integers and fraction symbols,
    respectively. All matches will be converted to integers, added up, and returned as a float. The number must
    be interpreted along the results of get_measurement() in order to make any meaning out of the quantity.

    '''

    # TODO: Write unit tests for fraction conversion.

    quantity = 0.0

    # RegEx patterns can be tested using: https://regexr.com/
    fraction_symbols = r'[\u00BC-\u00BE\u2150-\u215E\u2189]+'  # e.g ½
    written_fractions = r'(?:[1-9][0-9]*|0)\/[1-9][0-9]*'      # e.g 1/2
    integers = r'[0-9]+'

    # Test the RegEx patterns against the functions raw_string argument.
    find_fraction_symbols = re.search(fraction_symbols, raw_string)
    find_written_fractions = re.search(written_fractions, raw_string)
    find_integers = re.search(integers, raw_string)

    if bool(find_fraction_symbols):
        # Convert the matches to integers and add them to the quantity.
        quantity += unicodedata.numeric(find_fraction_symbols.group(0))

    if bool(find_written_fractions):
        # Use the fractions module to convert the written fraction to a float and add it to the quantity.
        fraction_string = find_written_fractions.group(0)
        quantity += float(Fraction(fraction_string))

    if bool(find_integers):
        quantity += int(find_integers.group(0))

    return quantity


def get_unit_of_measurement(raw_string: str = '100½ cups cheese', unit_list: list = list_of_units) -> str:
    '''Retrieve the measurement unit of a raw ingredient string.

    Simply matches the raw string against a RegEx pattern of all the units mentioned in "unit_list".
    If none of the measurements are returned, the function assumes that the ingredients are measured in
    discrete terms (i.e "1 whole egg") without any specific measurement

    '''

    search = re.search('|'.join(unit_list), raw_string)
    if search:
        return search.group(0)
    else:
        return 'whole'


# Show the results of the functions above in a dictionary.
def get_parsed_string(test_string: str = '½ pound shredded mozzarella cheese'):
    q = get_quantity(test_string)
    m = get_unit_of_measurement(test_string)
    d = get_ingredient_description(test_string)

    return {'quantity': q, 'measurement': m, 'description': d}
