from typing import Optional, Dict, Any, List, Union, Literal
import requests
from datetime import datetime

from .exceptions import AuthenticationError, APIError, VitesyError

class VitesyClient:
    """Main client for interacting with the Vitesy API."""
    
    def __init__(self, 
                 api_key: str, 
                 base_url: str = "https://v1.api.vitesyhub.com",
                 language: str = "en"):
        if not api_key:
            raise ValueError("API key is required")
            
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"x-api-key {api_key}",
            "Accept-Language": language
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the API with error handling."""
        try:
            response = self.session.request(
                method=method,
                url=f"{self.base_url}/{endpoint.lstrip('/')}",
                **kwargs
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            raise APIError(
                status_code=e.response.status_code,
                message=e.response.text
            )
        except requests.exceptions.RequestException as e:
            raise VitesyError(f"Request failed: {str(e)}")

    def get_device(self, device_id: str) -> Dict[str, Any]:
        """Get device information."""
        return self._make_request("GET", f"devices/{device_id}")

    def get_devices(self, 
                   user_id: Optional[str] = None,
                   place_id: Optional[str] = None,
                   expand: Optional[List[str]] = None,
                   language: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a list of devices matching the query parameters.

        Args:
            user_id: The ID of the user
            place_id: The ID of the place
            expand: List of attributes to join (e.g., ['goal', 'place', 'plant'])
            language: Override the default language for this request

        Returns:
            Dict containing the list of devices and related information

        Raises:
            APIError: If the query parameters are invalid
        """
        # At least one of user_id or place_id must be provided
        params = {}
        if user_id:
            params['user_id'] = user_id
        else:
            params['user_id'] = "me"
        if place_id:
            params['place_id'] = place_id
        if expand:
            params['expand'] = ','.join(expand)

        headers = {}
        if language:
            headers['Accept-Language'] = language

        return self._make_request(
            method="GET",
            endpoint="devices",
            params=params,
            headers=headers if headers else None
        ) 

    def get_sensors(self, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a list of all sensors.

        Args:
            language: Override the default language for this request

        Returns:
            Dict containing the list of sensors
        """
        headers = {}
        if language:
            headers['Accept-Language'] = language

        return self._make_request(
            method="GET",
            endpoint="sensors",
            headers=headers if headers else None
        ) 

    def query_measurements(
        self,
        device_id: Optional[str] = None,
        place_id: Optional[str] = None,
        from_date: Optional[Union[datetime, str]] = None,
        to_date: Optional[Union[datetime, str]] = None,
        latest: Optional[bool] = None,
        group_by: Optional[Literal["hour", "day", "week", "month"]] = None,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query measurements based on various filters.

        Args:
            device_id: The ID of the device
            place_id: The ID of the place
            from_date: Starting date-time of the measurements (ISO 8601 string or datetime object)
            to_date: Ending date-time of the measurements (ISO 8601 string or datetime object)
            latest: Only get the latest measurement
            group_by: Group measurements by time period ("hour", "day", "week", "month")
            language: Override the default language for this request

        Returns:
            Dict containing the list of measurements

        Raises:
            ValueError: If neither device_id nor place_id is provided
            APIError: If the query parameters are invalid
        """
        if not device_id and not place_id:
            raise ValueError("Either device_id or place_id must be provided")

        params = {}
        if device_id:
            params['device_id'] = device_id
        if place_id:
            params['place_id'] = place_id
        
        # Convert datetime objects to ISO 8601 strings
        if from_date:
            if isinstance(from_date, datetime):
                params['from'] = from_date.isoformat()
            else:
                params['from'] = from_date
                
        if to_date:
            if isinstance(to_date, datetime):
                params['to'] = to_date.isoformat()
            else:
                params['to'] = to_date

        if latest is not None:
            params['latest'] = str(latest).lower()
            
        if group_by:
            params['group_by'] = group_by

        headers = {}
        if language:
            headers['Accept-Language'] = language

        return self._make_request(
            method="GET",
            endpoint="measurements",
            params=params,
            headers=headers if headers else None
        ) 