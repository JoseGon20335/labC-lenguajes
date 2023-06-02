from createGraph import *


class Node:
    def __init__(this, name, rightLeaf, leftLeaf, nameOfTree=None):
        this.name = name
        this.rightLeaf = rightLeaf
        this.leftLeaf = leftLeaf
        this.numberId = None
        this.nullable = None
        this.firstPos = []
        this.lastPos = []
        this.followPos = []


class Tree(object):

    def __init__(this, postFix, nameOfTree) -> None:
        this.postFix = postFix
        this.nameOfTree = nameOfTree
        this.tree = None

    def postFixToTree(this):
        tree = []

        for c in this.postFix:
            if c == '*':
                temp = Node(c, None, None)
                temp.leftLeaf = tree.pop()
                tree.append(temp)

            elif c == '.':
                temp = Node(c, None, None)
                temp.rightLeaf = tree.pop()
                temp.leftLeaf = tree.pop()
                tree.append(temp)

            elif c == '|':
                temp = Node(c, None, None)
                temp.rightLeaf = tree.pop()
                temp.leftLeaf = tree.pop()
                tree.append(temp)

            elif c == '?':
                temp = Node('|', None, None)
                episilum = Node('ε', None, None)
                temp.leftLeaf = tree.pop()
                temp.rightLeaf = episilum
                tree.append(temp)

            elif c == '+':
                temp = Node('.', None, None)
                temp.leftLeaf = tree[-1]
                kleene = Node('*', None, None)
                kleene.leftLeaf = tree.pop()
                temp.rightLeaf = kleene
                tree.append(temp)

            else:
                temp = Node(c, None, None)
                tree.append(temp)
        this.tree = tree.pop()
        this.dataToGraph()
        return this.tree

    def dataToGraph(this):
        graficador = createGraph(data=this.tree, arbolName=this.nameOfTree)
        graficador.createTree()
