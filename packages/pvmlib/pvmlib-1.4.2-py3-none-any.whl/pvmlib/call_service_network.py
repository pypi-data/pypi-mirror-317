import requests
from typing import Any, Dict, Optional
from pvmlib.logger import LoggerSingleton
from pvmlib.response_exception import ResponseException
from pvmlib.response_ok import ResponseOK
import time
import functools

class RestClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.logger = LoggerSingleton().get_logger()

    def _handle_response(self, response: requests.Response, start_time: float):
        time_elapsed = int((time.time() - start_time) * 1000)
        transaction_id = response.headers.get("X-Request-ID", "N/A")
        if response.status_code >= 400:
            self.logger.error(f"HTTP error occurred: {response.status_code} for url {response.url}, response content: {response.text}")
            raise ResponseException(
                error_code="HTTP_ERROR",
                message=response.text,
                http_status_code=response.status_code,
                headers=response.headers
            )
        return ResponseOK(
            status_code=response.status_code,
            message=response.text,
            transaction_id=transaction_id,
            time_elapsed=time_elapsed,
            data=response.json() if response.content else None
        )

    def _log_and_handle_exceptions(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            try:
                self.logger.info(f"{func.__name__.upper()} request to {self.base_url}{args[0]} with params {kwargs.get('params')} and headers {kwargs.get('headers')}")
                response = func(self, *args, **kwargs)
                return self._handle_response(response, start_time).to_dict()
            except requests.HTTPError as e:
                self.logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                raise ResponseException(
                    error_code="HTTP_ERROR",
                    message=e.response.text,
                    http_status_code=e.response.status_code,
                    headers=e.response.headers
                )
            except requests.ConnectionError as e:
                self.logger.error(f"Connection error occurred: {str(e)}")
                raise ResponseException(
                    error_code="CONNECTION_ERROR",
                    message="Connection error occurred",
                    http_status_code=500,
                    headers={}
                )
            except requests.Timeout as e:
                self.logger.error(f"Timeout error occurred: {str(e)}")
                raise ResponseException(
                    error_code="TIMEOUT_ERROR",
                    message="Timeout error occurred",
                    http_status_code=500,
                    headers={}
                )
            except requests.RequestException as e:
                self.logger.error(f"Request error occurred: {str(e)}")
                raise ResponseException(
                    error_code="REQUEST_ERROR",
                    message="Request error occurred",
                    http_status_code=500,
                    headers={}
                )
            except Exception as e:
                self.logger.error(f"An unexpected error occurred: {str(e)}")
                raise ResponseException(
                    error_code="INTERNAL_ERROR",
                    message=str(e),
                    http_status_code=500,
                    headers={}
                )
        return wrapper

    @_log_and_handle_exceptions
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return requests.get(f"{self.base_url}{endpoint}", params=params, headers=headers)

    @_log_and_handle_exceptions
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return requests.post(f"{self.base_url}{endpoint}", data=data, json=json, headers=headers)

    @_log_and_handle_exceptions
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return requests.put(f"{self.base_url}{endpoint}", data=data, json=json, headers=headers)

    @_log_and_handle_exceptions
    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return requests.delete(f"{self.base_url}{endpoint}", headers=headers)