

from try_ds import Node
from loop import get_root_from_pickle


root:Node = get_root_from_pickle()


def get_next_nodes(search_str):
    if search_str == "":
        node = root
    else: 
        node = root.search(search_str.replace(" ", "").split(','))
    return [{'name': child.name, 'num_of_sections':len(child.get_all_songs())} for child in node.get_all_children_nodes()]

def get_songs(search_str, page_num, page_size):
    return list(root.search(search_str.replace(" ", "").split(',')).get_all_songs())[page_num*page_size: (page_num+1)*page_size ]

