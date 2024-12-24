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

    Args:
        root (Node): root node of tree we want to print
    """
    # get list[list[Node]] for easier printing
    node_levels: list[list[Node]] = assign_parent_and_get_node_levels(root)

    # recursively assign wideness scores (heuristic for how wide underscore strings will be)
    assign_wideness_scores(root)

    # initialize lines_to_print
    lines_to_print: list[str] = []
    
    # create underscore line for root node
    lines_to_print.append(get_underscore_line_for_root_node(root))

    for node_level in node_levels:

        # get pipe line
        pipe_line: str = get_pipe_line(node_level)
        lines_to_print.append(pipe_line)

        # get underscore line
        underscore_line: str = get_underscore_line(node_level, pipe_line)
        lines_to_print.append(underscore_line)

    # remove unnecessary columns
    lines_to_print: list[str] = remove_unneccesary_columns(lines_to_print)

    output_string: str = "\n".join(lines_to_print)

    print(dedent(output_string))