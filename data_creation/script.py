import requests
import re
import time
list_of_urls = list(map(lambda x: x.replace("\n", ""), (open("all_urls.txt","r"))))



def try_set(smth):
    try:
        return smth
    except: 
        return "UNKNOWN"

def get_info(content):
    chords = try_set(re.findall('\[ch\](.*?)\[', content))
    song_name = try_set(re.findall(r'\"byArtist\":.*?\"name.*?name\":\"(.*?)\"',content)[0])
    artist = try_set(re.findall(r'\"byArtist\":.*?name\":\"(.*?)\"',content)[0])
    return artist, song_name, chords
f = open("data/results.txt", 'w')
for api_url in list_of_urls:
    cache_url = f"http://webcache.googleusercontent.com/search?q=cache:{api_url}&strip=0&vwsrc=1"
    response = requests.get(api_url)
    content = str(response.content)
    artist, song_name, chords = get_info(content)
    to_write = f"{api_url} | {song_name} | {artist} |  {chords}"
    f.write(to_write)
    print(to_write)
    
    time.sleep(3)


