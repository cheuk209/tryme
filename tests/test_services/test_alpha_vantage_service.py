import pytest
import httpx
from app.services.alpha_vantage_service import AlphaVantageService
from app.models.commodity_data import Interval

@pytest.fixture
def alpha_vantage_service():
    return AlphaVantageService()

@pytest.mark.asyncio
async def test_get_commodity_data(alpha_vantage_service, mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "name": "Test Commodity",
        "unit": "USD",
        "data": [
            {"date": "2023-05-01", "value": 100.0},
            {"date": "2023-05-02", "value": 101.0},
        ]
    }

    mock_get = mocker.patch.object(httpx.AsyncClient, 'get', return_value=mock_response)

    result = await alpha_vantage_service.get_commodity_data("WTI", Interval.monthly)

    assert result["name"] == "Test Commodity"
    assert result["unit"] == "USD"
    assert len(result["data"]) == 2

    mock_get.assert_called_once_with(
        alpha_vantage_service.base_url,
        params={
            "function": "WTI",
            "interval": "monthly",
            "apikey": alpha_vantage_service.api_key
        }
    )

@pytest.mark.asyncio
async def test_get_commodity_data_http_error(alpha_vantage_service, mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError("HTTP Error", request=mocker.Mock(), response=mocker.Mock())

    mocker.patch.object(httpx.AsyncClient, 'get', return_value=mock_response)

    with pytest.raises(httpx.HTTPStatusError):
        await alpha_vantage_service.get_commodity_data("WTI", Interval.monthly)