import requests
from config.config import AUTH_URL, AUTH_CREDENTIALS, AUTH_HEADER

# AUTH_HEADER = None

def get_auth_header():
    """
    Authenticate with the Baubuddy API and retrieve an access token.
    Caches the token for subsequent requests.
    """
   
    url = AUTH_URL
    payload = AUTH_CREDENTIALS
    headers = AUTH_HEADER


    try:
        response = requests.post(url, json=payload, headers=headers)

        response.raise_for_status()

        # Extract access token from the response
        token = response.json().get("oauth", {}).get("access_token")
        if not token:
            raise Exception("Access token missing in response.")
        
        headers["Authorization"] = f"Bearer {token}"
        # headers["Authorization"] = f"Bearer 77c1544bc847e926ed7c157d0b748346cc14ca11"

        return headers
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to authenticate with Baubuddy API: {e}")
