from urllib.parse import urlparse
from aiohttp import web

_COOKIE_NAME_ = 'shipToken'

def get_host(url):
    """Get the hostname from a URL."""
    return urlparse(url).hostname

def is_subdomain(url, our_hosts):
    """Check if the given URL is a subdomain of one of our hosts."""
    subdomain = get_host(url)
    for host in our_hosts:
        if subdomain == host or subdomain.endswith('.' + host):
            return True
    return False

def get_ship_token(request: web.BaseRequest, as_cookie=False):
    """Get the ship token from the request headers."""
    if 'cookie' in request.headers:
        cookies = request.headers['cookie']
        cookie_list = [cookie.strip() for cookie in cookies.split(";")]
        for cookie in cookie_list:
            if cookie.startswith(f"{_COOKIE_NAME_}="):
                token = cookie.split("=")[1] # Extract the token
                if as_cookie:
                    return to_cookie(token)
                return token
    return None

def get_ship_token_from_response(response: web.Response, as_cookie=False):
    """
    Get the ship token from the response Set-Cookie headers.
    
    Args:
        response (web.Response): The response object to extract the token from.
        as_cookie (bool): If True, return the token wrapped as a cookie dict.

    Returns:
        str or dict: The token as a string, or a dict if `as_cookie` is True.
    """
    if 'Set-Cookie' in response.headers:
        cookies = response.headers['Set-Cookie']
        cookie_list = [cookie.strip() for cookie in cookies.split(",")]
        for cookie in cookie_list:
            if cookie.startswith(f"{_COOKIE_NAME_}="):
                token = cookie.split("=", 1)[1].split(";")[0]  # Extract the token
                if as_cookie:
                    return to_cookie(token)
                return token
    return None

def to_cookie(token: str):
    """Convert a token to a cookie string."""
    return {_COOKIE_NAME_: token}

def may_forward_ship_token(request: web.BaseRequest, dest_url: str):
    """Check if we are allowed to forward the ship token to the destination URL.
    We are allowed to forward the ship token if the destination URL is a subdomain of our host.
    """
    our_host = request.host
    if 'x-forwarded-host' in request.headers:
        our_host = [host.strip() for host in request.headers['x-forwarded-host'].split(',')]
    if is_subdomain(dest_url, our_host):
        return True
    return False