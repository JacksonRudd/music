
import enum
from operator import itemgetter
from typing import Iterable

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

def get_power(note):
    return [get_interval(note, 0),  get_interval(note, 7)]

def get_traid(note):
    return [get_interval(note, 0), get_interval(note, 4),  get_interval(note, 7)]

def get_minor_traid(note):
    return [get_interval(note, 0), get_interval(note, 3),  get_interval(note, 7)]

def get_notes_in_scale(note):
    return [get_interval(note, i) for i in [0, 2, 4, 5, 7, 9, 11]]

def get_root_and_extension(chord_name):
    if len(chord_name) == 1:
        return chord_name, ""
    if chord_name[1] not in ['#', 'b']:
        return chord_name[0], chord_name[1:]
    return convert_note_to_sharp(chord_name[0:2]), chord_name[2:]

def get_out_of_key_notes(start_of_scale, notes_in_song):
    return [song_note for song_note in notes_in_song if song_note not in get_notes_in_scale(start_of_scale)]

class Tonality(enum.Enum):
    MAJOR = 1
    MINOR = 2
    POWER = 3

class RelativeChord:
    def __init__(self, half_steps_from_root, extension, tonality):
        self.half_steps_from_root = half_steps_from_root
        self.extension = extension
        self.tonality = tonality

    def get_root_name(self):
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
        }[self.half_steps_from_root]
        return root

    def display(self):
        root_name = self.get_root_name()
        if self.tonality == Tonality.POWER:
            return root_name
        
        normal_tonality = {
            Tonality.MAJOR: ["ONE", "FOUR", "FIVE"],
            Tonality.MINOR: ['TWO', "THREE", "SIX"],
        }        
        return root_name if root_name in normal_tonality[self.tonality] else f"{self.tonality.name} {root_name}"
        
class Chord:
    def __init__(self, chord_name):
        self.root, self.extension = get_root_and_extension(chord_name)
        if self.extension == '5':
            self.tonality = Tonality.POWER
        else:    
            is_minor = "m" in chord_name and 'maj' not in chord_name
            self.tonality = Tonality.MINOR if is_minor else Tonality.MAJOR
                
    def get_notes_in_chord(self):
        return {
            Tonality.POWER: get_power, 
            Tonality.MAJOR: get_traid, 
            Tonality.MINOR: get_minor_traid
        }[self.tonality](self.root)
    
    def get_interval_from_root_of_key(self, key):
        return get_interval_between(key, self.root)

    def get_relative_chord(self, key):
        return RelativeChord(self.get_interval_from_root_of_key(key), self.extension, self.tonality)

class RelativeChordProgression:

    def __init__(self, chords: Iterable[RelativeChord]):
        self.chords = chords

    def get_formatted_relative_chords(self):
        return [chord.display() for chord in self.chords]

class ConcreteChordProgression:

    def __init__(self, list_of_raw_names):
        self.chords = [Chord(raw_name) for raw_name in list_of_raw_names]
        self.key, self.percent_out = self._find_key()


    def get_relative_progression(self) -> RelativeChordProgression: 
        return RelativeChordProgression([concrete_chord.get_relative_chord(self.key) for concrete_chord in self.chords])

    def _find_key(self):
        'used in init'
        notes_in_song = self._get_notes_in_list_of_chord()
        d = {start_of_scale: len(get_out_of_key_notes(start_of_scale, notes_in_song)) for start_of_scale in notes}
        key, num_out_of_key = min(d.items(), key=itemgetter(1))
        percentage_off = int(num_out_of_key/len(notes_in_song)*100)
        return key, percentage_off

    def _get_notes_in_list_of_chord(self):
        'helper for find key'
        to_return = []
        for set_of_notes in [chord.get_notes_in_chord() for chord in self.chords]:
            to_return.extend(set_of_notes)
        return list(to_return)

        

