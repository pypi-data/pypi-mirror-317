import requests

def shorten_url(url):
    response = requests.get("http://tinyurl.com/api-create.php?url="+url)
    return response.text

url = "https://auth.geeksforgeeks.org/user/josal/"
short_url = shorten_url(url)
print(f"The shortened URL is: {short_url}")