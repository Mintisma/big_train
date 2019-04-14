import re


def url2date(url):
    pattern = r'.+/(\d{4}-*\d{2}-*\d{2})/.+'
    match_obj = re.match(pattern, url)
    date = match_obj.group(1).replace('-', '')
    return date