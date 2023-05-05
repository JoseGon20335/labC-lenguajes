from graphviz import Digraph
from collections import deque


class createGraph(object):

    def __init__(this, data=None) -> None:
        this.data = data

    def createTree(this):
        tree = Digraph('results/Tree', 'resultado')
        tree.graph_attr['rankdir'] = 'TB'
        tree = this.addLeaftToTree(tree, this.data)
        tree.view()

    def addLeaftToTree(this, tree, data):
        if data is None:
            return tree
        tree.node(str(id(data)), str(data.name), shape='circle')
        if data.leftLeaf is not None:
            tree = this.addLeaftToTree(tree, data.leftLeaf)
            tree.edge(str(id(data)), str(id(data.leftLeaf)))
        if data.rightLeaf is not None:
            tree = this.addLeaftToTree(tree, data.rightLeaf)
            tree.edge(str(id(data)), str(id(data.rightLeaf)))

        return tree
