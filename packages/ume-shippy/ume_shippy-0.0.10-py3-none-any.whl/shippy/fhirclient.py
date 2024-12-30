import aiohttp
from aiohttp import web
from urllib.parse import urlencode
from auth import get_ship_token_from_response

class UnauthorizedException(Exception):
    """Custom exception to represent a 403 Unauthorized error."""

    def __init__(self, message="Access denied. Unauthorized request.", status_code=403):
        """
        Initialize the exception with a message and status code.

        Args:
            message (str): The error message.
            status_code (int): HTTP status code, defaults to 403.
        """
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}")

class BadRequestException(Exception):
    """Custom exception to represent a 400 Bad Request error."""

    def __init__(self, message="Bad request. The server could not understand the request.", status_code=400):
        """
        Initialize the exception with a message and status code.

        Args:
            message (str): The error message.
            status_code (int): HTTP status code, defaults to 400.
        """
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}")

class FHIRClient:

    def __init__(self, 
                fhir_server: str,
                auth_server: str, 
                username: str = None, 
                password:str = None,
                auth_token: str = None):

        self.auth_server = auth_server
        self.fhir_server = fhir_server
        self.username = username
        self.password = password
        self.auth_token = auth_token

    async def authenticate(self):
        if self.auth_token:
            return self.auth_token
        elif self.username and self.password:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.auth_server, auth=aiohttp.BasicAuth(self.username, self.password)) as response:
                    response.raise_for_status()
                    self.auth_token = await response.text()
                    return self.auth_token
        else:
            raise BadRequestException("Cannot authenticate. No credentials provided.")

    async def _load_get(self, url: str, cycle_break: bool = False) -> dict:
        """Load a resource from the FHIR server using a GET request."""
        if not url.startswith('http'):
            url = f"{self.fhir_server}/{url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'Authorization': f"Bearer {self.auth_token}"}) as response:
                if response.status == 200:
                    # update token if it has changed
                    self.auth_token = get_ship_token_from_response(response)
                    # return response as json
                    return await response.json()
                elif response.status == 401:
                    if cycle_break:
                        raise web.HTTPUnauthorized(text="You are not authorized to access this resource.")
                    else:
                        # make sure token is no longer used
                        self.auth_token = None
                        try:
                            await self.authenticate()
                        except BadRequestException:
                            raise web.HTTPUnauthorized(text="You are not authorized to access this resource.")
                        return await self.load(url, True)
                elif response.status == 404:
                    print('{} [HTTP Status 404]'.format(url))
                    raise web.HTTPNotFound(text="The requested resource was not found.")
                elif response.status == 500:
                    raise web.HTTPInternalServerError(text="An error occured. Please try again later.")
                elif response.status == 503:
                    raise web.HTTPServiceUnavailable(text="The service is currently unavailable. Please try again later.")
                elif response.status == 504:
                    raise web.HTTPGatewayTimeout(text="The service timed out. Please try again later.")
                elif response.status == 429:
                    raise web.HTTPTooManyRequests(text="You have exceeded the rate limit. Please try again later.")
                elif response.status == 400:
                    raise web.HTTPBadRequest(text="The request was malformed.")
                elif response.status == 403:
                    raise web.HTTPForbidden(text="You are not allowed to access this resource.")
                elif response.status == 405: 
                    raise web.HTTPMethodNotAllowed(text="The requested method is not allowed.")
                else:
                    raise web.HTTPException(text=f"HTTP Error: {response.status}")

    async def _load_post(self, url: str, payload: dict, cycle_break: bool = False) -> dict:
        """Load a resource from the FHIR server using a POST request."""
        if not url.startswith('http'):
            url = f"{self.fhir_server}/{url}"

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, 
                json=payload, 
                headers={'Authorization': f"Bearer {self.auth_token}"}
            ) as response:
                if response.status == 200:
                    # Update token if it has changed
                    self.auth_token = get_ship_token_from_response(response)
                    # Return response as JSON
                    return await response.json()
                elif response.status == 401:
                    if cycle_break:
                        raise web.HTTPUnauthorized(text="You are not authorized to access this resource.")
                    else:
                        # Reset token and re-authenticate
                        self.auth_token = None
                        try:
                            await self.authenticate()
                        except BadRequestException:
                            raise web.HTTPUnauthorized(text="You are not authorized to access this resource.")
                        return await self._load_post(url, payload, True)
                elif response.status == 404:
                    print(f'{url} [HTTP Status 404]')
                    raise web.HTTPNotFound(text="The requested resource was not found.")
                elif response.status == 500:
                    raise web.HTTPInternalServerError(text="An error occurred. Please try again later.")
                elif response.status == 503:
                    raise web.HTTPServiceUnavailable(text="The service is currently unavailable. Please try again later.")
                elif response.status == 504:
                    raise web.HTTPGatewayTimeout(text="The service timed out. Please try again later.")
                elif response.status == 429:
                    raise web.HTTPTooManyRequests(text="You have exceeded the rate limit. Please try again later.")
                elif response.status == 400:
                    raise web.HTTPBadRequest(text="The request was malformed.")
                elif response.status == 403:
                    raise web.HTTPForbidden(text="You are not allowed to access this resource.")
                elif response.status == 405:
                    raise web.HTTPMethodNotAllowed(text="The requested method is not allowed.")
                else:
                    raise web.HTTPException(text=f"HTTP Error: {response.status}")

    async def resource(self, resource_type: str, resource_id: str):
        """Get a FHIR resource by type and ID."""
        url = self.fhir_server
        if not url.endswith('/'):
            url += '/'
        url += f'{resource_type}/{resource_id}'
        return await self._load_get(url)
    
    async def search(self, resource_type: str, query_params: dict = None):
        """Get a FHIR search."""
        url = self.fhir_server
        if not url.endswith('/'):
            url += '/'
        url += f'{resource_type}'
        
        return await self._load_post(url, query_params)
