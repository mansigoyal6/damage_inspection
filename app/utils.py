import re

def validate_image_url(url):
    return bool(re.match(r'^https?:\/\/.*\.(jpg|jpeg|png)$', url, re.IGNORECASE))