# coding: utf-8
"""
  Copyright (c) 2024 Vipas.AI
 
  All rights reserved. This program and the accompanying materials
  are made available under the terms of a proprietary license.
"""
from typing import Dict, Optional, Any
from urllib.parse import urljoin

from vipas.config import Config
from vipas import _rest
from vipas.logger import LoggerClient
import pybreaker
from ratelimit import limits, sleep_and_retry
from vipas.exceptions import ClientException


class ChallengeClient:
    """Client for interacting with the Vipas.AI Challenge API.
    
    This client provides methods to interact with challenge-related endpoints,
    including rate limiting and circuit breaker functionality.
    
    Attributes:
        DEFAULT_CALLS_PER_MINUTE (int): Default rate limit for API calls
        DEFAULT_FAIL_MAX (int): Default maximum consecutive failures before circuit breaks
        DEFAULT_RESET_TIMEOUT (int): Default timeout in seconds before circuit resets
    """
    
    DEFAULT_CALLS_PER_MINUTE = 20
    DEFAULT_FAIL_MAX = 10
    DEFAULT_RESET_TIMEOUT = 60

    def __init__(
        self,
        configuration: Optional[Config] = None,
        calls_per_minute: int = DEFAULT_CALLS_PER_MINUTE,
        fail_max: int = DEFAULT_FAIL_MAX,
        reset_timeout: int = DEFAULT_RESET_TIMEOUT
    ) -> None:
        """Initialize the ChallengeClient.
        
        Args:
            configuration: Custom configuration object. If None, uses default Config.
            calls_per_minute: Maximum number of API calls allowed per minute.
            fail_max: Maximum number of consecutive failures before circuit breaks.
            reset_timeout: Time in seconds before circuit breaker resets.
        """
        self.configuration = configuration or Config()
        self.rest_client = _rest.RESTClientObject(self.configuration)
        self.logger = LoggerClient(__name__)
        
        self._configure_decorators(
            calls_per_minute=calls_per_minute,
            fail_max=fail_max,
            reset_timeout=reset_timeout
        )

    def _configure_decorators(
        self,
        calls_per_minute: int,
        fail_max: int,
        reset_timeout: int
    ) -> None:
        """Configure rate limiting and circuit breaker decorators.
        
        Args:
            calls_per_minute: Maximum number of API calls allowed per minute.
            fail_max: Maximum number of consecutive failures before circuit breaks.
            reset_timeout: Time in seconds before circuit breaker resets.
        """
        self.breaker = pybreaker.CircuitBreaker(
            fail_max=fail_max,
            reset_timeout=reset_timeout
        )
        self.rate_limit = limits(calls=calls_per_minute, period=60)

        # Apply decorators to methods
        self.get_challenge_submissions = self._apply_decorators(
            self.get_challenge_submissions
        )

    def _apply_decorators(self, func):
        """Apply all decorators to a function in the correct order.
        
        Args:
            func: Function to decorate.
            
        Returns:
            Decorated function with circuit breaker, rate limiting and retry logic.
        """
        func = self.breaker(func)
        func = self.rate_limit(func)
        func = sleep_and_retry(func)
        return func

    def _call_api(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API.
        
        Args:
            method: HTTP method to use.
            url: API endpoint URL.
            params: Query parameters to include in the request.
            body: Request body data.
            headers: Additional headers to include in the request.
            
        Returns:
            API response data as a dictionary.
            
        Raises:
            ClientException: If the API request fails.
        """
        try:
            response_data = self.rest_client._get_challenge_submission(
                method=method,
                url=url,
                params=params,
                body=body,
                headers=headers
            )
            return response_data
        except ClientException as e:
            self.logger.error(f"API call failed: {str(e)}")
            raise

    def get_challenge_submissions(self, challenge_id: str) -> Dict[str, Any]:
        """Get submissions for a specific challenge.
        
        Args:
            challenge_id: Unique identifier of the challenge.
            
        Returns:
            Dictionary containing challenge submission data.
            
        Raises:
            ClientException: If the API request fails.
        """
        params = {"challenge_id": challenge_id}
        url = urljoin(self.configuration.host, "challenge/submissions")
        
        _header_params: Dict[str, Optional[str]] =  {}
        _header_params['vps-auth-token'] = self.configuration.get_vps_auth_token()
        
        self.logger.info(f"Fetching submissions for challenge {challenge_id}, you can check the submissions in the challenge-stats page here https://vipas.ai/challenge/{challenge_id}/stats.")
        return self._call_api(
            method="GET",
            url=url,
            params=params,
            headers=_header_params
        )