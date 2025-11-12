import requests
import json
import allure
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseAPI:
    """
    Base API class for making HTTP requests with built-in retry, logging, and Allure reporting.
    """

    def __init__(self, base_url, timeout=30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = self._create_session()
        logger.info(f"Initialized BaseAPI with base_url: {self.base_url}")

    def _create_session(self):
        """
        Create a requests session with retry strategy.
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    @allure.step("GET request to {endpoint}")
    def get(self, endpoint, params=None, headers=None):
        """
        Make a GET request.
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET request to: {url}")
        logger.debug(f"Parameters: {params}")
        logger.debug(f"Headers: {headers}")
        
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            self._log_response(response)
            return response
        except Exception as e:
            logger.error(f"GET request failed: {str(e)}")
            raise

    @allure.step("POST request to {endpoint}")
    def post(self, endpoint, data=None, json_data=None, headers=None):
        """
        Make a POST request.
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to: {url}")
        logger.debug(f"Data: {data}")
        logger.debug(f"JSON: {json_data}")
        logger.debug(f"Headers: {headers}")
        
        try:
            response = self.session.post(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout
            )
            self._log_response(response)
            return response
        except Exception as e:
            logger.error(f"POST request failed: {str(e)}")
            raise

    @allure.step("PUT request to {endpoint}")
    def put(self, endpoint, data=None, json_data=None, headers=None):
        """
        Make a PUT request.
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT request to: {url}")
        logger.debug(f"Data: {data}")
        logger.debug(f"JSON: {json_data}")
        logger.debug(f"Headers: {headers}")
        
        try:
            response = self.session.put(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout
            )
            self._log_response(response)
            return response
        except Exception as e:
            logger.error(f"PUT request failed: {str(e)}")
            raise

    @allure.step("DELETE request to {endpoint}")
    def delete(self, endpoint, headers=None):
        """
        Make a DELETE request.
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE request to: {url}")
        logger.debug(f"Headers: {headers}")
        
        try:
            response = self.session.delete(
                url,
                headers=headers,
                timeout=self.timeout
            )
            self._log_response(response)
            return response
        except Exception as e:
            logger.error(f"DELETE request failed: {str(e)}")
            raise

    @allure.step("PATCH request to {endpoint}")
    def patch(self, endpoint, data=None, json_data=None, headers=None):
        """
        Make a PATCH request.
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PATCH request to: {url}")
        logger.debug(f"Data: {data}")
        logger.debug(f"JSON: {json_data}")
        logger.debug(f"Headers: {headers}")
        
        try:
            response = self.session.patch(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout
            )
            self._log_response(response)
            return response
        except Exception as e:
            logger.error(f"PATCH request failed: {str(e)}")
            raise

    def _log_response(self, response):
        """
        Log response details and attach to Allure report.
        """
        logger.info(f"Response Status: {response.status_code}")
        logger.debug(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            logger.debug(f"Response Body: {json.dumps(response_json, indent=2)}")
            allure.attach(
                json.dumps(response_json, indent=2),
                name="Response JSON",
                attachment_type=allure.attachment_type.JSON
            )
        except ValueError:
            logger.debug(f"Response Text: {response.text}")
            allure.attach(
                response.text,
                name="Response Text",
                attachment_type=allure.attachment_type.TEXT
            )
        
        allure.attach(
            f"Status Code: {response.status_code}",
            name="Status Code",
            attachment_type=allure.attachment_type.TEXT
        )

    def verify_status_code(self, response, expected_code):
        """
        Verify response status code.
        """
        actual_code = response.status_code
        logger.info(f"Verifying status code: Expected={expected_code}, Actual={actual_code}")
        assert actual_code == expected_code, f"Expected {expected_code} but got {actual_code}"

    def get_json_response(self, response):
        """
        Get JSON response body.
        """
        try:
            return response.json()
        except ValueError:
            logger.error("Response is not valid JSON")
            return None
