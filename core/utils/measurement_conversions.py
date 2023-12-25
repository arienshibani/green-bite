def convert_measurement_to_kg(measurement: str, amount: float) -> float:
    '''A switch statement, chooses the appropriate conversion function based on the string argument.'''
    switch_statement = {
        'pound': pounds_to_metric,
        'pounds': pounds_to_metric,
        'ounce': ounce_to_metric,
        'ounces': ounce_to_metric,
        'oz': ounce_to_metric,
        'cup': cups_to_metric,
        'cups': cups_to_metric,
        'tablespoon': tablespoons_to_metric,
        'tablespoons': tablespoons_to_metric,
        'tbsp': tablespoons_to_metric,
        'teaspoons': teaspoons_to_metric,
        'teaspoon': teaspoons_to_metric,
        'tsp': teaspoons_to_metric,
        'tsps': teaspoons_to_metric,
        'kilogram': amount,
        'kilograms': amount,
        'kg': amount,
        'kgs': amount,
        'gram': lambda a: a / 1000,
        'grams': lambda a: a / 1000,
        'g': lambda a: a / 1000
    }

    chosen_conversion = switch_statement.get(
        measurement, lambda a: f'Error: Measure "{measurement}" not included in function: convert_measuremnt_to_kg().')

    try:
        return chosen_conversion(amount)
    except TypeError:
        return amount


def pounds_to_metric(pounds: float = 1) -> float:
    '''Converts pounds to kilograms'''
    return round(pounds * 0.45359237, 3)


def ounce_to_metric(ounce: float = 1) -> float:
    '''Converts ounces to kilograms.'''
    return round(ounce * 0.0283495231, 3)


'''The measures below are problematic as they are not measures of mass, but measures of volume. 
In order to get the exact values one needs the mass density of the substance in question. '''


def cups_to_metric(cups: float = 1) -> float:
    '''Converts cups to kilograms. (Formula based on sugar) '''
    kilograms = cups / 4.960
    return kilograms


def tablespoons_to_metric(tbsp: float = 1) -> float:
    '''Converts tablespoons to kilograms. (Formula based on water) '''
    kilograms = tbsp / 67
    return kilograms


def teaspoons_to_metric(tsp: float = 1) -> float:
    '''Converts teaspoons to kilograms.'''
    kilograms = tsp / 123
    return kilograms
