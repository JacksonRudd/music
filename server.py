

from try_ds import Node
from loop import get_root_from_pickle


root:Node = get_root_from_pickle()


def get_next_nodes(search_str):
    return [{'name': child.name, 'num_of_sections':len(child.get_all_songs())} for child in root.search(search_str.replace(" ", "").split(',')).get_all_children_nodes()]

def get_songs(search_str, page_num, page_size):
    return root.search(search_str.replace(" ", "").split(',')).get_all_songs()[page_num*page_size: (page_num+1)*page_size ]

