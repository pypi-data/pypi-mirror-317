

import unittest
from src.pprint_tree.models import Node
from src.pprint_tree.helpers.string_helper import get_underscore_component

class TestStringHelper(unittest.TestCase):

    def test_get_underscore_component__no_children(self):
        node = Node("apple")
        self.assertEqual(get_underscore_component(node), "apple")

    def test_get_underscore_component__one_child(self):
        node = Node("apple")
        node.wideness_score = 10
        node.children.append(Node("hi"))
        self.assertEqual(get_underscore_component(node).strip(), "apple")

    def test_get_underscore_component__2_children(self):
        node1, node2, node3 = Node("apple"), Node("orange"), Node("pear")
        node1.wideness_score = 9
        node1.children = [node2, node3]
        self.assertEqual(get_underscore_component(node1).strip(), "__apple__")
