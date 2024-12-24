
# pprint_tree
prints tree (where nodes have multiple children) in human readable format

# Installation
```
pip install pprint_tree
```

# Quickstart
```python
class Node:
    def __init__(self, val):
        self.val = val
        self.children = []

root = Node("apple")
root.children.append(Node("orange"))
root.children.append(Node("pear"))
root.children.append(Node("pineapple"))
root.children.append(Node("banana"))
root.children[0].children.append(Node("orange1"))
root.children[0].children.append(Node("orange2"))
root.children[1].children.append(Node("pear1"))
root.children[1].children[0].children.append(Node("pear2"))
root.children[1].children[0].children[0].children.append(Node("pear3"))
root.children[1].children[0].children[0].children.append(Node("pear4"))
root.children[2].children.append(Node("kiwi"))
root.children[2].children.append(Node("avocado"))
root.children[2].children.append(Node("cherry tomatoes"))
root.children[2].children.append(Node("golden kiwi"))
root.children[2].children.append(Node("soup"))


from pprint_tree import pprint_tree

pprint_tree(root)

"""
            ____________________________________________apple__________________________________________
            |                        |                                   |                            |
    _____orange_______             pear           ___________________pineapple__________________   banana
    |                |              |             |       |            |              |        |
orange1          orange2         pear1          kiwi  avocado  cherry tomatoes  golden kiwi  soup
                                   |
                             ____pear2_______
                             |              |
                          pear3          pear4
"""
```
