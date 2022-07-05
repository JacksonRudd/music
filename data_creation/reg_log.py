import re
import time
from tkinter import W


w = open('data_creation/content.txt', 'r').read()

# m = re.findall(, w)

# print(m)

def try_set(smth):
    try:
        return smth
    except: 
        return "UNKNOWN"

def get_info(content):
    regex_for_parts = r'\\\\r\\\\n\[([0-9A-Za-z ,]*?)\]\\\\r\\\\n'
    regex_for_chords = '\[ch\](.*?)\['
    chords_regs = re.compile("(%s|%s)" % (regex_for_parts, regex_for_chords)).findall(content)
    chords = [(len(reg[1]) > 0)*"s_" + reg[1]+reg[2] for reg in chords_regs]
    song_name = try_set(re.findall(r'\"byArtist\":.*?\"name.*?name\":\"(.*?)\"',content)[0])
    artist = try_set(re.findall(r'\"byArtist\":.*?name\":\"(.*?)\"',content)[0])
    return artist, song_name, chords


print(get_info(w))