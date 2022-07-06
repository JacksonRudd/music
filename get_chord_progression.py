
def append_return(list, item):
    new_list = list.copy()
    new_list.insert(0, item)
    return new_list

def get_all_subsequences(chords):
    for i in range(len(chords)):
        for j in range(0,len(chords)+1):
            yield chords[i:i+j]

def get_all_repeats(subs):
    for sub in subs: 
        for i in range(2,10):
            repeated_part = sub[0:int(len(sub)/i)]
            if repeated_part*i == sub and len(repeated_part)>2 :
                yield {"sub":repeated_part, "size":len(repeated_part), "repeats": i}

def get_chord_progression(chords):
    subs = get_all_subsequences(chords)
    repeats = list(get_all_repeats(subs))
    if repeats == []:
        return None
    return max(repeats, key=lambda x : x["repeats"])

