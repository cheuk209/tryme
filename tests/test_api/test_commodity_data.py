import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.models.commodity_data import Commodity, CommodityData, Interval
from app.services.alpha_vantage_service import AlphaVantageService
print("Available routes:")
for route in app.routes:
    print(f"{route.methods} {route.path}")

client = TestClient(app)

def test_root():
    response = client.get("/")
    print(f"Root response: {response.status_code}")
    assert response.status_code != 404, "FastAPI app is not responding"
# Mock data for testing
mock_commodity = Commodity(
    name="Crude Oil Prices WTI",
    interval=Interval.monthly,
    unit="dollars per barrel",
    data=[
        CommodityData(date="2024-06-01", value=79.77),
        CommodityData(date="2024-05-01", value=80.02),
        CommodityData(date="2024-04-01", value=85.35),
        CommodityData(date="2024-03-01", value=81.28),
    ]
)

class MockAlphaVantageService:
    async def get_commodity_data(self, function: str, interval: Interval):
        return mock_commodity

@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[AlphaVantageService] = MockAlphaVantageService
    yield
    app.dependency_overrides.clear()

def test_get_commodity_data():
    
    response = client.get("/api/v1/commodity?function=WTI&interval=monthly")
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 200
    data = response.json()
    assert data["commodity"]["name"] == "Crude Oil Prices WTI"
    assert len(data["commodity"]["data"]) == 4

def test_get_commodity_data_with_date_range():
    response = client.get("/api/v1/commodity?function=WTI&interval=monthly&start_date=2024-04-01&end_date=2024-05-31")
    assert response.status_code == 200
    data = response.json()
    assert len(data["commodity"]["data"]) == 2
    assert data["filtered_range"] == "2024-04-01 to 2024-05-31"

def test_get_commodity_data_invalid_interval():
    response = client.get("/api/v1/commodity?function=WTI&interval=invalid")
    assert response.status_code == 422  # Unprocessable Entity

def test_get_commodity_data_invalid_date_format():
    response = client.get("/api/v1/commodity?function=WTI&interval=monthly&start_date=2024-13-01")
    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.parametrize("function", ["WTI", "BRENT"])
def test_get_commodity_data_different_functions(function):
    response = client.get(f"/api/v1/commodity?function={function}&interval=monthly")
    assert response.status_code == 200
    data = response.json()
    assert data["commodity"]["name"] == "Crude Oil Prices WTI"  # This would change with real data

def test_get_commodity_data_future_date_range():
    today = datetime.now().date()
    future_date = (today + timedelta(days=365)).isoformat()
    response = client.get(f"/api/v1/commodity?function=WTI&interval=monthly&start_date={future_date}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["commodity"]["data"]) == 0