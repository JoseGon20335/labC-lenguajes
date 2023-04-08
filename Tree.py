from createGraph import *


class Node:
    def __init__(this, name, rightLeaf, leftLeaf):
        this.name = name
        this.rightLeaf = rightLeaf
        this.leftLeaf = leftLeaf


class Tree(object):

    def __init__(this, postFix) -> None:
        this.postFix = postFix
        this.tree = None

    def postFixToTree(this):
        tree = []

        for c in this.postFix:
            print("c", c)
            if c == '*':
                print("entro *", c)
                temp = Node(c, None, None)
                temp.leftLeaf = tree.pop()
                tree.append(temp)

            elif c == '.':
                print("entro .", c)
                temp = Node(c, None, None)
                temp.rightLeaf = tree.pop()
                temp.leftLeaf = tree.pop()
                tree.append(temp)

            elif c == '|':
                print("entro |", c)
                temp = Node(c, None, None)
                temp.rightLeaf = tree.pop()
                temp.leftLeaf = tree.pop()
                tree.append(temp)

            elif c == '?':
                print("entro ?", c)
                temp = Node(c, None, None)
                episilum = Node('ε', None, None)
                temp.leftLeaf = tree.pop()
                temp.rightLeaf = episilum
                tree.append(temp)

            elif c == '+':
                print("entro +", c)
                temp = Node(c, None, None)
                temp.leftLeaf = tree[-1]
                kleene = Node('*', None, None)
                kleene.leftLeaf = tree.pop()
                temp.rightLeaf = kleene
                tree.append(temp)

            else:
                print("entro else", c)
                temp = Node(c, None, None)
                tree.append(temp)
        this.tree = tree.pop()
        this.dataToGraph()
        return this.tree

    def dataToGraph(this):
        print("data", this.tree)
        graficador = createGraph(data=this.tree)
        graficador.createTree()
