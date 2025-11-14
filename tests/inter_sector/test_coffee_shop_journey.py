import requests
import time
import os

# Service names are from the docker-compose.yml file
HUB_URL = "http://hub-api:8000"
FINANCE_URL = "http://finance-api:8000"

def test_coffee_shop_journey():
    """
    Runs a full user journey:
    1. Create a project in 'hub'
    2. Check that a corresponding transaction is created in 'finance'
    """
    
    # Step 1: Wait for services to be online
    # (In a real test, this would be in a pytest fixture)
    
    # Step 2: Create a project in the Hub service
    project_response = requests.post(
        f"{HUB_URL}/v1/projects",
        json={"name": "Test Coffee Shop", "budget": 100}
    )
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # Step 3: Check the Finance service for the transaction
    time.sleep(1) # Give time for event to propagate
    
    finance_response = requests.get(
        f"{FINANCE_URL}/v1/transactions",
        params={"project_id": project_id}
    )
    assert finance_response.status_code == 200
    transactions = finance_response.json()
    assert len(transactions) == 1
    assert transactions["amount"] == -100
    assert transactions["description"] == "Initial project budget for Test Coffee Shop"