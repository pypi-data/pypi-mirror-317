import os
import pytest
from vitesy import VitesyClient
from datetime import datetime, timedelta

# Skip all tests in this module if no API key is provided
pytestmark = pytest.mark.skipif(
    not os.getenv("VITESY_API_KEY"),
    reason="VITESY_API_KEY environment variable not set"
)

@pytest.fixture
def integration_client():
    api_key = os.getenv("VITESY_API_KEY")
    return VitesyClient(api_key=api_key)

class TestVitesyClientIntegration:
    def test_get_devices(self, integration_client):
        response = integration_client.get_devices()
        assert len(response) > 0

    def test_get_sensors(self, integration_client):
        response = integration_client.get_sensors()
        assert len(response) > 0

    def test_query_measurements(self, integration_client):
        # Query last hour's measurements
        to_date = datetime.utcnow()
        from_date = to_date - timedelta(hours=1)
        
        response = integration_client.query_measurements(
            from_date=from_date,
            to_date=to_date,
            group_by="hour"
        )
        assert len(response) > 0