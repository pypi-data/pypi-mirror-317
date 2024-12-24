from dataclasses import dataclass
from typing import Optional

class Node:
    def __init__(self, val):
        self.val = val
        self.children: list[Node] = []

        """
        Given Node('hello') and string:
        "    __________hello__________    "
             l                       r

            - l = left_index (inclusive)
            - r = right_index (inclusive)
        """
        self.parent: Optional[Node] = None
        self.left_index: Optional[int] = None
        self.right_index: Optional[int] = None

        self.child_node_to_pipe_index_map: dict[Node, int] = {}

        # no children => wideness_score of self.width
        # wideness_score = sum of wideness_scores of children + self.width
        self.wideness_score: int = 0

    def __str__(self):
        parent_val = self.parent.val if self.parent else None
        attrs: str = f"val={self.val}, parent={parent_val}"

        if None not in (self.left_index, self.right_index):
            attrs += f", left_index={self.left_index}, right_index={self.right_index}"

        attrs += f", wideness_score={self.wideness_score}"

        return f"Node({attrs})"
    
    def __repr__(self):
        return self.__str__()
