import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.services.alpha_vantage_service import AlphaVantageService
from app.models.commodity_data import Interval, Commodity, CommodityData

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Please hire me"}

mock_commodity_data = {
    "name": "Test Commodity",
    "interval": "weekly",
    "unit": "USD",
    "data": [
        {"date": "2023-01-01", "value": "100.0"},
        {"date": "2023-02-01", "value": "101.0"},
        {"date": "2023-03-01", "value": "102.0"},
        {"date": "2023-04-01", "value": "."}
    ]
}

mock_commodity_response = Commodity(
            name = mock_commodity_data["name"],
            interval = mock_commodity_data["interval"],
            unit = mock_commodity_data["unit"],
            data = [CommodityData(**item) for item in mock_commodity_data["data"]]
        )

@pytest.fixture # mocking and making commodity data available for tests
def mock_alpha_vantage_service(monkeypatch):
    async def mock_get_commodity_data(self, function, interval):
        valid_commodities = ['foo', 'bar']  # Add all valid commodities here
        if function not in valid_commodities:
            raise ValueError(f"Invalid commodity: {function}")
        mock_commodity_response.interval = interval
        return mock_commodity_response
    monkeypatch.setattr("app.services.alpha_vantage_service.AlphaVantageService.get_commodity_data", mock_get_commodity_data)

def test_get_commodity_data_success(mock_alpha_vantage_service):
    response = client.get("/api/v1/commodity/foo?interval=weekly")
    data = response.json()
    print("What is data pls,", data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Commodity"
    assert data["interval"] == "weekly"
    assert data["unit"] == "USD"
    assert len(data["data"]) == 4

@pytest.mark.parametrize("interval", [Interval.daily, Interval.monthly, Interval.weekly])
def test_get_commodity_data_different_intervals(mock_alpha_vantage_service, interval):
    print("What is int value", dir(interval))
    response = client.get(f"/api/v1/commodity/bar?interval={interval.value}")
    data = response.json()
    print("lets see", data)
    assert response.status_code == 200
    assert data["interval"] == interval.value

def test_get_commodity_data_invalid_interval(mock_alpha_vantage_service):
    response = client.get("/api/v1/commodity/foo?interval=invalid")
    error_detail = response.json()["detail"]
    assert any(error["loc"] == ["query", "interval"] for error in error_detail)

def test_get_commodity_data_missing_interval(mock_alpha_vantage_service):
    response = client.get("/api/v1/commodity/foo")
    assert response.status_code == 200  # Assuming it defaults to monthly
    data = response.json()
    assert data["interval"] == "monthly"

def test_get_commodity_data_invalid_commodity(mock_alpha_vantage_service):
    response = client.get("/api/v1/commodity/INVALID?interval=weekly")
    data = response.json()
    print(data)
    assert response.status_code == 400
    assert "Invalid commodity: INVALID" in data['detail']

def test_get_commodity_data_with_date_filter(mock_alpha_vantage_service):
    response = client.get("/api/v1/commodity/foo?interval=weekly&start_date=2023-02-01&end_date=2023-03-01")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["data"][0]["date"] == "2023-02-01"
    assert data["data"][1]["date"] == "2023-03-01"

def test_get_commodity_data_invalid_date_format(mock_alpha_vantage_service):
    response = client.get("/api/v1/commodity/WTI?interval=weekly&start_date=2023/01/01")
    assert response.status_code == 400  # Bad Request

def test_get_commodity_data_future_date(mock_alpha_vantage_service):
    future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    response = client.get(f"/api/v1/commodity/foo?interval=weekly&end_date={future_date}")
    assert response.status_code == 200
    data = response.json()
    assert all(datetime.strptime(item["date"], "%Y-%m-%d") <= datetime.now() for item in data["data"])

def test_get_commodity_data_contains_null_value(mock_alpha_vantage_service):
    response = client.get("/api/v1/commodity/foo?interval=weekly&start_date=2023-04-01")
    assert response.status_code == 200