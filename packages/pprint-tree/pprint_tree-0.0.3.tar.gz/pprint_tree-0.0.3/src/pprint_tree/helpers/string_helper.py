"""
Contains string manipulation helpers
"""

from ..models import Node

def get_underscore_component(node: Node) -> str:
    """
    Args:
        node (Node): one single node

    Returns:
        (str) eg. "___apple___"
    """
    if len(node.children) <= 1:
        return str(node.val).center(node.wideness_score)
    return str(node.val).center(node.wideness_score, "_") 

def get_underscore_line_for_root_node(root: Node, seed: int):
    """
    Gets underscore line just for root node. Start with lots of spaces on the left
    """
    root_str: str = get_underscore_component(root)
    root.left_index = seed
    root.right_index = seed + len(root_str) - 1
    return " " * seed + root_str

def get_underscore_line(
    node_level: list[Node],
    pipe_line: str,
    seed: int,
) -> str:
    """
    Args:
        node_level (list[Node]): list of Node objects in one level
    Returns:
        (str): line to be printed out 
    """
    chars: list[str] = [" "] * seed * 5
    pipe_indexes: list[int] = [index for index, val in enumerate(pipe_line) if val=="|"]

    for parent_node in node_level:
        for child_node in parent_node.children:
            node_str: str = get_underscore_component(child_node)
            pipe_index: int = pipe_indexes.pop(0)
            start_index = pipe_index - len(node_str) // 2
            end_index = start_index + len(node_str)
            child_node.left_index = start_index
            child_node.right_index = end_index - 1
            chars[start_index: end_index] = list(node_str)

    return "".join(chars).rstrip()


def get_pipe_indexes(parent_node: Node) -> list[int]:
    """
    Get indexes of pipes for one single parent node, based on .left_index and .right_index

    Returns:
        (list[int]): each int is a pipe_index, corresponding to one child node
    """
    children: list[Node] = parent_node.children

    if len(children) == 0:
        return []
    
    if len(children) == 1:
        return [ (parent_node.left_index + parent_node.right_index ) // 2 ]
    
    # initialize list of pipe indexes that respect wideness_score
    pipe_indexes: list[int] = [parent_node.left_index]

    for index in range(len(children) - 1):
        left_child = children[index]
        right_child = children[index + 1]
        pipe_indexes.append(
            pipe_indexes[-1] + 
            left_child.wideness_score // 2 + 
            right_child.wideness_score // 2
        )
    # breakpoint()
    while True:
        # expand this to fit parent's left_index and right_index as much as possible
        new_pipe_indexes = [pi + inc for pi, inc in zip(pipe_indexes, range(100))]

        # check if this exceeds parent_node's left and right bound
        if new_pipe_indexes[-1] > parent_node.right_index:
            new_pipe_indexes[-1] = parent_node.right_index
            return new_pipe_indexes
            
        pipe_indexes = new_pipe_indexes

def get_pipe_line(node_level: list[Node], seed:int) -> str:
    """
    Args:
        node_level (list[Node]): list of parent nodes

    Returns:
        (str): pipe_line for child nodes of parent nodes in node_level
        eg. "          |         |          |        | "
    """
    chars: list[str] = [" "] * seed * 5

    for parent_node in node_level:
    
        # initialize list of pipe indexes that respect wideness_score
        pipe_indexes: list[int] = get_pipe_indexes(parent_node)
        
        for pipe_index in pipe_indexes:
            chars[pipe_index] = "|"

    return "".join(chars).rstrip()

def remove_unneccesary_columns(lines_to_print: list[str]) -> list[str]:
    """
    Columns are deliberately made long at first to accomodate screwups. Remove them now.
    """
    col_indexes_to_remove: set[int] = set()
    col_index: int = 0

    longest_line_length: int = max(len(line) for line in lines_to_print)

    while col_index < longest_line_length:
        char_set: set[str] = set()

        for line in lines_to_print:
            if col_index < len(line):
                char_set.add(line[col_index])
            if col_index - 1 >= 0 and col_index - 1 < len(line):
                char_set.add(line[col_index - 1])
            if col_index + 1 < len(line):
                char_set.add(line[col_index + 1])

        # if char_set only contains " " or "_", remove
        if char_set == {" "} or char_set == {"_"} or char_set == {" ", "_"}:
            col_indexes_to_remove.add(col_index)

        col_index += 1

    line_lists: list[list[str]] = [list(line) for line in lines_to_print]
    for line_list in line_lists:
        for col_index in col_indexes_to_remove:
            if col_index >= len(line_list):
                continue
            line_list[col_index] = ""

    return ["".join(line_list) for line_list in line_lists]
