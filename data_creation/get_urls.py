import requests
import re
all_urls = []
total_pages = 200 #851559
misses = []
for i in range(total_pages): 
    try:
        progress_percent = i*100/total_pages
        print(int(progress_percent)*"-" + (100 - int(progress_percent))*"_", progress_percent)
        api_url = f"https://www.ultimate-guitar.com/explore?page={i}"
        response = requests.get(api_url)
        content = str(response.content)
        all_urls.extend(re.findall('(https://tabs.ultimate-guitar.com/tab/.*?)&quot', content))
    except:
        misses.append(i)


file=open('all_urls.txt','w')
for items in all_urls:
    file.writelines([items, '\n'])

file=open('misses.txt','w')
for items in misses:
    file.writelines([items, '\n'])
