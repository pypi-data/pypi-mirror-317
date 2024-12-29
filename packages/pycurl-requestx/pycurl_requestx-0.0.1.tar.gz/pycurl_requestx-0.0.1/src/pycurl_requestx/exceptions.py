class PycurlRequestXError(Exception):
    """Base exception for pycurl-requestx."""
    pass

class RequestError(PycurlRequestXError):
    """Raised when an HTTP request fails."""
    pass

