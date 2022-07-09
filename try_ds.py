

from typing import Iterable


class Node:

    def __init__(self, name):
        self.name = name
        self.children = {}
        self.songs = set()

    def get_or_create_node(self, chord_name) -> 'Node':
        if chord_name not in self.children.keys():
            self.children[chord_name] = Node(chord_name)     
        return self.children[chord_name]

    def add_to_try(self, section, song_name, index=0):
        this_chord = section[index]
        next_node =  self.get_or_create_node(this_chord)
        if index  == len(section) - 1:
            next_node.songs.add(song_name)
        else:
            next_node.add_to_try(section, song_name, index + 1)
        return self
    
    def get_all_songs(self):
        to_return = set()
        to_return.update(self.songs)
        for child in self.get_all_children_nodes():
            to_return.update(child.get_all_songs())
        return to_return

    def get_all_children_nodes(self) -> Iterable['Node']:
        return list(self.children.values())
    
    def pchildren(self)-> Iterable[str]:
        [print(x.name) for x in self.get_all_children_nodes()]
        return self

    def psongs(self) -> 'Node':
        [print(song) for song in self.get_all_songs()]
        return self

    def pdown(self, tab_level=0) -> 'Node':
        print(" "*tab_level, self.name)
        print(" "*tab_level, self.get_all_songs())
        print()
        for child in self.get_all_children_nodes():
            child.pdown(tab_level=tab_level+1)
        return self

    def has_child(self, child_name) -> bool:
        return child_name in self.children.keys()

    def search(self, progression) -> 'Node':
        if len(progression) == 0:
            return self
        first_chord = progression[0]
        return self.children[first_chord].search(progression[1:]) if self.has_child(first_chord) else None

