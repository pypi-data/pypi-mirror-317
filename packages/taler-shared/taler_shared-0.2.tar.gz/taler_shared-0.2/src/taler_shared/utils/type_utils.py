from urllib.parse import urlparse
import os

def isUrl(path):
    try:
        parsedUrl = urlparse(path)
        # Check if the scheme (protocol) is either 'http' or 'https'
        isValid = all([
            parsedUrl.scheme,
            parsedUrl.netloc,
            parsedUrl.scheme in ['http', 'https']
        ])

        return isValid 
        
    except ValueError:
        return False