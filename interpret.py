import pandas as pd
from operator import itemgetter

def get_df():
    with open('data/results.txt') as f:
        lines = f.readlines()[0].split("]h")
        lines = [line.replace('[', '') for line in lines]
    return pd.DataFrame( [line.split('|') for line in lines])

df = get_df()
def get_song(i):
    row = df.iloc[i]
    return row[1], row[2], row[3].replace("'", '').replace(" ", '').split(',')


notes = ["C", "C#", "D","D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def get_note(index):
    return notes[index%len(notes)]

def get_interval(note, interval):
    return get_note(notes.index(note) + interval)

def get_interval_between(start, end):
    mod =  (notes.index(end) - notes.index(start)) % 12
    return mod if mod > 0 else (12 + mod) % 12


def convert_note_to_sharp(note):
    if "b" not in note:
        return note
    else:
        return notes[notes.index(note[0]) - 1]

def get_root_and_extension(name):
    if len(name) == 1:
        return name, ""
    if name[1] not in ['#', 'b']:
        return name[0], name[1:]
    return convert_note_to_sharp(name[0:2]), name[2:]

def is_minor(chord_name):
    return "m" in chord_name and 'maj' not in chord_name

def get_traid(note):
    note = convert_note_to_sharp(note)
    return [get_interval(note, 0), get_interval(note, 4),  get_interval(note, 7)]

def get_minor_traid(note):
    note = convert_note_to_sharp(note)
    return [get_interval(note, 0), get_interval(note, 3),  get_interval(note, 7)]

def get_traid_in_chord(chord_name):
    root, _ = get_root_and_extension(chord_name)
    return get_minor_traid(root) if is_minor(chord_name) else get_traid(root)



def get_notes_in_chord(chord_name):
    to_return = get_traid_in_chord(chord_name)
    root, extension = get_root_and_extension(chord_name)
    return to_return
    

def get_notes_in_scale(note):
    return [get_interval(note, i) for i in [0, 2, 4, 5, 7, 9, 11]]

def get_notes_in_list_of_chord(list_of_chord_names):
    to_return = []
    for set_of_notes in [get_notes_in_chord(chord_name) for chord_name in list_of_chord_names]:
        to_return.extend(set_of_notes)
    return list(to_return)

def get_out_of_key_notes(start_of_scale, notes_in_song):
    return [song_note for song_note in notes_in_song if song_note not in get_notes_in_scale(start_of_scale)]

def get_key(chords):
    notes_in_song = get_notes_in_list_of_chord(chords)
    d = {start_of_scale: len(get_out_of_key_notes(start_of_scale, notes_in_song)) for start_of_scale in notes}
    key, num_out_of_key = min(d.items(), key=itemgetter(1))
    percentage_off = int(num_out_of_key/len(notes_in_song)*100)
    return key, percentage_off


def get_relative_information(key, chord_name):
    root, extension = get_root_and_extension(chord_name)
    return {"half_steps_from_root":get_interval_between(key, root), "extension": extension, "is_minor": is_minor(chord_name), 'chord_name': chord_name}

def get_relative_chords(chords):
    return [get_relative_information(get_key(chords)[0], chord) for chord in chords]

def display(half_steps_from_root, is_minor, extension):
    root = {
        0: "ONE",
        1: "FLAT TWO",
        2: "TWO",
        3: "FLAT THREE",
        4: "THREE",
        5: "FOUR",
        6: "FLAT FIVE",
        7: "FIVE",
        8: "FLAT SIX",
        9: "SIX",
        10: "FLAT SEVEN",
        11: "FLAT SEVEN",        
    }[half_steps_from_root]
    tonality = "MIN" if is_minor else "MAJ"
    if is_minor ^ (root in ["ONE", "FOUR", "FIVE"]):
        return root
    return f"{tonality} {root}"    
    


def get_formatted_relative_chords(chords):
    return [display(x['half_steps_from_root'], x['is_minor'], x['extension']) for x in get_relative_chords(chords)]

def append_return(list, item):
    new_list = list.copy()
    new_list.insert(0, item)
    return new_list

def get_all_subsequences(chords):
    for i in range(len(chords)):
        for j in range(0,len(chords) - i):
            yield chords[i:i+j]

def get_all_repeats(subs):
    for sub in subs: 
        for i in range(2,10):
            if sub[0:int(len(sub)/i)]*i == sub and len(sub) > 1:
                yield (sub[0:int(len(sub)/i)], i)

for i in range(10):
    name, artist, chords = get_song(i)
    if len(chords)< 2: continue
    print(name, artist)
    #print(get_formatted_relative_chords(chords))
    print(get_key(chords))
    subs = get_all_subsequences(get_formatted_relative_chords(chords))
    repeats = get_all_repeats(subs)
    print(max(repeats, key=lambda x: x[1]))
    print()

