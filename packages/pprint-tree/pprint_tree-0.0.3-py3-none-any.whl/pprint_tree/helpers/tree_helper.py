"""
Contains helper function relating to trees and travesal
"""

from typing import Deque, Any, Optional, Tuple
from collections import deque

from ..models import Node


def assign_parent_and_get_node_levels(root: Node) -> list[list[Node]]:
    """
    1) assign the .parent attribute for all nodes
    2) get list of nodes for each level

    Args:
        root (Node): root node of tree
    Returns
        (list[list[Node]]): list of nodes for each level
    """
    # intiialize node_levels (we return this at the end)
    node_levels: list[list[Node]] = []

    # intitialize deque for traversal
    NodeParentLevel = tuple[Node, Optional[Node], int]
    node_dq: Deque[NodeParentLevel] = deque([(root, None, 0)])

    # begin traversal
    while node_dq:
        current_node: Node
        parent_node: Optional[Node]
        current_level: int 
        current_node, parent_node, current_level = node_dq.popleft()

        # set .parent attribute to Node
        current_node.parent = parent_node

        # check if level exists in node_levels
        if len(node_levels) < current_level + 1:
            node_levels.append([])
        
        # add node into correct level
        node_levels[current_level].append(current_node)

        # add current_node's children back into deque for further traversal
        for child_node in current_node.children:
            node_dq.append(
                (child_node, current_node, current_level + 1)
            )

    return node_levels


def assign_wideness_scores(node: Node) -> Node:
    """
    Recursively assigns wideness_score (heuristic used to determine length of underscore string)

    .wideness_score (int):
        if no children, wideness_score = width of value
        if have children, wideness_score = width of value + sum(wideness_scores of children)
    """
    if not node.children:
        node.wideness_score = len(str(node.val)) * 2
        return
    
    for child_node in node.children:
        assign_wideness_scores(child_node)
    
    node.wideness_score = (
        len(str(node.val)) +
        sum(child_node.wideness_score for child_node in node.children)
    )