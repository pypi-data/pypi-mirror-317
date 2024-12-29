from .exceptions import RequestError

def handle_response(response_code: int, response_data: str):
    if response_code >= 400:
        raise RequestError(f"Request failed with status code {response_code}: {response_data}")
