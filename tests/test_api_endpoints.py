from fastapi.testclient import TestClient
from main import app  # Ensure the app instance is imported correctly

client = TestClient(app)

def test_parse_ingredient():
    # Test a valid ingredient parsing
    response = client.get("/parse/ingredient/1%20kg%20of%20cheese")
    assert response.status_code == 200
    data = response.json()

    assert "inputIngredientString" in data
    assert "sustainabilityScore" in data

def test_score_calculation():
    # Test scoring multiple ingredients
    response = client.post("/score?ingredients=1%20cups%20of%20milk&ingredients=3%20tablespoons%20sugar&ingredients=2%20tablespoons%20cornstarch")
    assert response.status_code == 200
    assert isinstance(response.json(), float)
