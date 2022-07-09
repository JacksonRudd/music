from get_chord_progression import get_all_subsequences
from interpret import get_formatted_relative_chords
import pandas as pd
import pickle 

from try_ds import Node

def get_df():
    with open('./data_creation/data/results.txt') as f:
        lines = f.readlines()
    return pd.DataFrame( [line.split('|') for line in lines])

df = get_df()

def get_song(i):
    row = df.iloc[i]
    return row[1], row[2], row[3].replace("'", '').replace(" ", '').replace("[", "").replace("]","").replace("\n", "").split(',')

def get_root(song_num):
    root = Node('root')
    for i in range(song_num):
        try:
            name, artist, chords = get_song(i)
            chords.insert(0, 'section_start')
            idxs = [i for i, v in enumerate(chords, 0) if "s_" in v]   # calculating indices
            song = {chords[i]:chords[i+1:j] for i, j in zip(idxs, idxs[1:]+[len(chords)])}
            for section in song: 
                section_chords = song[section]
                rel_chords = get_formatted_relative_chords(section_chords)
                subseqs = [rel_chords[i: i+5] for i in range(len(rel_chords)-1)]
                for seq in subseqs:
                    root.add_to_try(seq, str((name, artist, section)))
        except Exception as e:
            print("error", name, artist)  
            print(e)

    return root

def get_root_from_pickle():
    return pickle.load(open('root.pkl', 'rb'))

if __name__=="__main__":
    root = get_root(5000)
    filehandler = open('root.pkl', 'wb') 
    pickle.dump(root, filehandler)