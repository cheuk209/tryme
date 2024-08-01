import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.services.alpha_vantage_service import AlphaVantageService
from app.models.commodity_data import Interval

client = TestClient(app)

@pytest.fixture
def mock_alpha_vantage_service(mocker):
    mock_service = mocker.Mock(spec=AlphaVantageService)
    mock_service.get_commodity_data.return_value = {
        "name": "Test Commodity",
        "unit": "USD",
        "data": [
            {"date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"), "value": 100.0 + i}
            for i in range(10)
        ]
    }
    return mock_service

@pytest.mark.asyncio
async def test_get_commodity_data(mock_alpha_vantage_service):
    app.dependency_overrides[AlphaVantageService] = lambda: mock_alpha_vantage_service
    
    response = client.get("/commodity/WTI?interval=monthly")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Commodity"
    assert data["interval"] == "monthly"
    assert data["unit"] == "USD"
    assert len(data["data"]) == 10

@pytest.mark.asyncio
async def test_get_commodity_data_with_date_filter(mock_alpha_vantage_service):
    app.dependency_overrides[AlphaVantageService] = lambda: mock_alpha_vantage_service
    
    start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    response = client.get(f"/commodity/WTI?interval=monthly&start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 6  # 5 days + today

@pytest.mark.asyncio
async def test_get_commodity_data_invalid_date(mock_alpha_vantage_service):
    app.dependency_overrides[AlphaVantageService] = lambda: mock_alpha_vantage_service
    
    response = client.get("/commodity/WTI?interval=monthly&start_date=invalid-date")
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_get_commodity_data_service_error(mock_alpha_vantage_service):
    mock_alpha_vantage_service.get_commodity_data.side_effect = Exception("Service error")
    app.dependency_overrides[AlphaVantageService] = lambda: mock_alpha_vantage_service
    
    response = client.get("/commodity/WTI?interval=monthly")
    assert response.status_code == 500