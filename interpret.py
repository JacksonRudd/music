import pandas as pd
from operator import itemgetter

def get_df():
    with open('results.txt') as f:
        lines = f.readlines()[0].split("]h")
        lines = [line.replace('[', '') for line in lines]
    return pd.DataFrame( [line.split('|') for line in lines])

notes = ["C", "C#", "D","D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def get_note(index):
    return notes[index%len(notes)]

def get_interval(note, interval):
    return get_note(notes.index(note) + interval)

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


df = get_df()
for i in range(100):

    row = df.iloc[i]
    chords = row[3].replace("'", '').replace(" ", '').split(',')
    if len(chords)< 2:
        continue
    print(row[1], row[2])
    print(chords)

    print(get_key(chords))
    print()

