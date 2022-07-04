import requests
import re

list_of_urls = list(map(lambda x: x.replace("\n", ""), (open("all_urls.txt","r"))))


for api_url in list_of_urls:
    cache_url = f"http://webcache.googleusercontent.com/search?q=cache:{api_url}&strip=0&vwsrc=1"

    response = requests.get(cache_url)
    content = str(response.content)
    print(re.findall('\[ch\](.*?)\[', content))


