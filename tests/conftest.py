import nltk
import pytest

'''
Conftest.py is a file that contains all the fixtures that are used in the test files.
Fixtures are functions that run before the unit tests in order to set up the environment for the tests to run.
'''


@pytest.fixture(scope='session', autouse=True)
def setup_nltk_data():
    # Download the NLTK data needed for the tests, if not already present
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
