import requests
import re
import time

from reg_log import get_info

list_of_urls = list(map(lambda x: x.replace("\n", ""), (open("data/all_urls.txt","r"))))

f = open("data/results.txt", 'w')
for api_url in list_of_urls:
    cache_url = f"http://webcache.googleusercontent.com/search?q=cache:{api_url}&strip=0&vwsrc=1"
    response = requests.get(api_url)
    content = str(response.content)
    artist, song_name, chords = get_info(content)
    to_write = f"{api_url} | {song_name} | {artist} |  {chords}"
    f.write(to_write)
    f.write('\n')
    print(to_write)
    time.sleep(3)


