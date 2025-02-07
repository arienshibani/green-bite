import nltk
import pytest


@pytest.fixture(scope='session', autouse=True)
def setup_nltk_data():
    # Download the NLTK data needed for the tests, if not already present
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
