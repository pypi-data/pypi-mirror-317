from textwrap import dedent
from pprint import pprint

from .models import Node
from .helpers.tree_helper import (
    assign_parent_and_get_node_levels,
    assign_wideness_scores,
)
from .helpers.string_helper import *

def pprint_tree(root: Node) -> None:
    """
    prints a tree (where nodes have multiple children) in human readable format

    Example Node class definition:

    class Node:
        def __init__(self, val: Any):
            self.val: Any = val
            self.children: list[Node] = []

    Args:
        root (Node): root node of tree we want to print
    """
    seed: int = 200
    for i in range(20):
        try:
            try_pprint_tree(root, seed=seed)
            return
        except:
            seed *= 2

def try_pprint_tree(root: Node, seed=200) -> None:
    """
    attempt to pprint_tree. might raise error. if error, retry with larger seed
    """
    # get list[list[Node]] for easier printing
    node_levels: list[list[Node]] = assign_parent_and_get_node_levels(root)

    # recursively assign wideness scores (heuristic for how wide underscore strings will be)
    assign_wideness_scores(root)

    # initialize lines_to_print
    lines_to_print: list[str] = []
    
    # create underscore line for root node
    lines_to_print.append(get_underscore_line_for_root_node(root, seed=seed))

    for node_level in node_levels:

        # get pipe line
        pipe_line: str = get_pipe_line(node_level, seed=seed)
        lines_to_print.append(pipe_line)

        # get underscore line
        underscore_line: str = get_underscore_line(node_level, pipe_line, seed=seed)
        lines_to_print.append(underscore_line)

    # remove unnecessary columns
    lines_to_print: list[str] = remove_unneccesary_columns(lines_to_print)

    output_string: str = "\n".join(lines_to_print)

    print(dedent(output_string))