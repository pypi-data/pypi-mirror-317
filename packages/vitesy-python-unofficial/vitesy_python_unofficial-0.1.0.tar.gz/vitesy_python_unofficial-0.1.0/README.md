# Vitesy Python SDK

An unofficial Python SDK for interacting with the Vitesy API platform.

## Disclaimer

This is an **unofficial** SDK and is not affiliated with, maintained, authorized, endorsed, or sponsored by Vitesy or any of its affiliates. This is an independent and unofficial project. All product and company names are trademarks™ or registered® trademarks of their respective holders.

## Installation

```bash
pip install vitesy-python-unofficial
```

## Usage

### Initialize the Client

```python
from vitesy import VitesyClient

# Initialize with default language (English)
client = VitesyClient(api_key='your_api_key')

# Or initialize with a specific language
client = VitesyClient(api_key='your_api_key', language='it')
```

### Available Endpoints

#### Get Devices

```python
# Get devices for the authenticated user
devices = client.get_devices()

# Get devices for a specific user
devices = client.get_devices(user_id="user-id")

# Get devices for a specific place
devices = client.get_devices(place_id="place-id")

# Get devices with expanded information
devices = client.get_devices(
    expand=["goal", "place", "plant"]
)
```

#### Get Device Details

```python
device = client.get_device("device-id")
```

#### Get Sensors

```python
# Get all sensors
sensors = client.get_sensors()

# Get sensors with specific language
sensors = client.get_sensors(language="it")
```

#### Query Measurements

```python
from datetime import datetime, timedelta

# Get latest measurements for a device
measurements = client.query_measurements(
    device_id="device-id",
    latest=True
)

# Get hourly measurements for the last 24 hours
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=1)

measurements = client.query_measurements(
    device_id="device-id",
    from_date=start_date,
    to_date=end_date,
    group_by="hour"
)

# Get measurements for a specific place
measurements = client.query_measurements(
    place_id="place-id",
    group_by="day"
)
```

### Error Handling

```python
from vitesy import VitesyError, AuthenticationError, APIError

try:
    devices = client.get_devices()
except AuthenticationError:
    print("Invalid API key")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
except VitesyError as e:
    print(f"General error: {str(e)}")
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vitesy-python-sdk.git
cd vitesy-python-sdk
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest
```

### Publishing to PyPI

1. Build the package:
```bash
python -m pip install --upgrade build
python -m build
```

2. Upload to TestPyPI (optional):
```bash
python -m pip install --upgrade twine
python -m twine upload --repository testpypi dist/*
```

3. Upload to PyPI:
```bash
python -m twine upload dist/*
```

## Testing

The SDK includes both unit tests and integration tests.

### Running Unit Tests

Unit tests can be run without any API credentials:

```bash
pytest -m "not integration"
```

### Running Integration Tests

Integration tests require valid API credentials. To run them:

1. Set your API key as an environment variable:
```bash
export VITESY_API_KEY="your-api-key"
```

2. Run the integration tests:
```bash
pytest tests/integration/
```

Or run all tests (both unit and integration):
```bash
pytest
```

### Test Structure

- `tests/test_client.py`: Unit tests for the client
- `tests/integration/test_integration.py`: Integration tests with the actual API
- `tests/conftest.py`: Shared test fixtures and configuration

The test suite uses pytest and includes:
- Basic client initialization tests
- API endpoint tests with mocked responses
- Error handling tests
- Integration tests with the actual API
- Language support tests

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
