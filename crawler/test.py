from urllib.parse import urlparse, parse_qs

url = "http://www.ty-magnet.com/contactus.html"

print(urlparse(url).path)
