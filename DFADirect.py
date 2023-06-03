from createGraphAfdDirect import *
from Tree import *


class transition:
    def __init__(self, state, symbol):
        self.state = state
        self.symbol = symbol


class NODE:
    def __init__(self, name, symbol, related):
        self.name = name
        self.symbol = symbol
        self.related = related
        self.transition_to = []
        self.token = ''

    def add_transition(self, transition_to, transition_name):
        transitionTemp = transition(transition_to, transition_name)
        self.transition_to.append(transitionTemp)

    def add_token(self, token):
        self.token = token


class DFADirect:
    def __init__(self):
        self.expectStates = []
        self.states = []
        self.alphabet = []
        self.start_state = None
        self.final_states = []
        self.state_counter = 0
        self.leafs = []
        self.tokensFinals = []

    def convert(self, postfix):
        postfix.append('#')
        postfix.append('.')
        tree = Tree(postFix=postfix, nameOfTree='treeDFADirect')
        tree.postFixToTree()
        self.afdDirecto(tree)
        print(tree)
        self.print_result()
        createGraphAfdDirect(self).createGraph()

    def afdDirecto(self, tree):
        self.countLeaf(tree.tree)
        self.nullable(tree.tree)
        self.firstPos(tree.tree)
        self.lastPos(tree.tree)
        self.followPos(tree.tree)
        self.symbolDirect(tree.tree)

        conta = 0

        addState = None
        isFinal = False
        for firstPos in tree.tree.firstPos:
            if '#' in firstPos.name:
                isFinal = True

        if isFinal:
            addState = NODE(str(conta), 3, tree.tree.firstPos)
            self.final_states.append(addState)
        else:
            addState = NODE(str(conta), 2, tree.tree.firstPos)

        self.start_state = addState
        self.states.append(addState)
        conta += 1

        for state in self.states:
            for symbol in self.alphabet:
                temp = []
                for position in state.related:
                    if position.name == symbol:
                        for position2 in position.followPos:
                            temp.append(position2)
                        # temp.extend(position.followPos)
                        temp = list(set(temp))

                if len(temp) > 0:

                    dontRepeat = self.dontRepeat(temp, self.states)

                    if dontRepeat == True:

                        tokenAdd = ''
                        for tempState in temp:
                            if '#' in tempState.name:
                                tokenAdd = tempState.name
                                self.tokensFinals.append(tempState.name)

                        if tokenAdd != '':
                            addState = NODE(str(conta), 1, temp)
                            addState.add_token(tokenAdd)
                            self.final_states.append(addState)
                        else:
                            addState = NODE(str(conta), 0, temp)

                        self.states.append(addState)
                        conta += 1

                        temp = []
                        index = self.states.index(state)
                        self.states[index].add_transition(addState, symbol)

                    else:
                        state.add_transition(dontRepeat, symbol)

        return self.states

    def countLeaf(self, node):
        if node.leftLeaf == None and node.rightLeaf == None and node.name != 'ε':
            self.state_counter += 1
            node.numberId = self.state_counter
            self.leafs.append(node)
        else:
            if node.leftLeaf != None:
                self.countLeaf(node.leftLeaf)
            if node.rightLeaf != None:
                self.countLeaf(node.rightLeaf)

    def nullable(self, node):
        if node.leftLeaf == None and node.rightLeaf == None and node.name == 'ε':
            node.nullable = True
        elif node.leftLeaf == None and node.rightLeaf == None:
            node.nullable = False
        else:
            if node.name == '*' or node.name == '+' or node.name == '?':
                self.nullable(node.leftLeaf)
                node.nullable = True
            elif node.name == '.' or node.name == '|':
                self.nullable(node.leftLeaf)
                self.nullable(node.rightLeaf)

                if node.name == '.':
                    if node.leftLeaf.nullable == True and node.rightLeaf.nullable == True:
                        node.nullable = True
                    else:
                        node.nullable = False
                elif node.name == '|':
                    if node.leftLeaf.nullable == True or node.rightLeaf.nullable == True:
                        node.nullable = True
                    else:
                        node.nullable = False

    def firstPos(self, node):
        if node.leftLeaf == None and node.rightLeaf == None and node.name == 'ε':
            node.firstPos = []
        elif node.leftLeaf == None and node.rightLeaf == None:
            node.firstPos.append(node)
        else:
            if node.name == '*' or node.name == '+' or node.name == '?':
                self.firstPos(node.leftLeaf)
                node.firstPos = node.leftLeaf.firstPos
            elif node.name == '.' or node.name == '|':
                self.firstPos(node.leftLeaf)
                self.firstPos(node.rightLeaf)

                if node.name == '.':
                    if node.leftLeaf.nullable == True:
                        node.firstPos = node.leftLeaf.firstPos + node.rightLeaf.firstPos

                    elif node.leftLeaf.nullable == False:
                        node.firstPos = node.leftLeaf.firstPos

                elif node.name == '|':
                    node.firstPos = node.leftLeaf.firstPos + node.rightLeaf.firstPos

    def lastPos(self, node):
        if node.leftLeaf == None and node.rightLeaf == None and node.name == 'ε':
            node.lastPos = []
        elif node.leftLeaf == None and node.rightLeaf == None:
            node.lastPos.append(node)
        else:
            if node.name == '*' or node.name == '+' or node.name == '?':
                self.lastPos(node.leftLeaf)
                node.lastPos = node.leftLeaf.lastPos
            elif node.name == '.' or node.name == '|':
                self.lastPos(node.leftLeaf)
                self.lastPos(node.rightLeaf)

                if node.name == '.' and node.rightLeaf.nullable == True:
                    node.lastPos = node.leftLeaf.lastPos + node.rightLeaf.lastPos
                else:
                    node.lastPos = node.rightLeaf.lastPos

                if node.name == '|':
                    node.lastPos = node.leftLeaf.lastPos + node.rightLeaf.lastPos

    def followPos(self, node):
        if node.name == '.':
            for position in node.leftLeaf.lastPos:
                for position2 in node.rightLeaf.firstPos:
                    for leafsTemp in self.leafs:
                        if leafsTemp.numberId == position.numberId:
                            dontRepeat = self.dontRepeatNode(
                                position2, leafsTemp.followPos)
                            if dontRepeat == True:
                                leafsTemp.followPos.append(position2)
            self.followPos(node.leftLeaf)
            self.followPos(node.rightLeaf)

        elif node.name == '*':
            for position in node.lastPos:
                for position2 in node.firstPos:

                    for leafsTemp in self.leafs:
                        if leafsTemp.numberId == position.numberId:
                            dontRepeat = self.dontRepeatNode(
                                position2, leafsTemp.followPos)
                            if dontRepeat == True:
                                leafsTemp.followPos.append(position2)
            self.followPos(node.leftLeaf)

        elif node.name == '|':
            self.followPos(node.leftLeaf)
            self.followPos(node.rightLeaf)

    def symbolDirect(self, node):
        if node.leftLeaf == None and node.rightLeaf == None:
            if node.name != 'ε' and node.name[:1] != '#':
                if node.name not in self.alphabet:
                    self.alphabet.append(node.name)
        else:
            if node.leftLeaf != None:
                self.symbolDirect(node.leftLeaf)
            if node.rightLeaf != None:
                self.symbolDirect(node.rightLeaf)

    def dontRepeat(self, states, afdActual):
        for node in afdActual:
            if len(node.related) == len(states):
                temp = 0
                for state in states:
                    if state in node.related:
                        temp = temp + 1
                if temp == len(states):
                    return node
        return True

    def dontRepeatNode(self, states, afdActual):
        for node in afdActual:
            if node.name == states.name:
                return node
        return True

    def print_result(self):
        print('_________AFDirecto_________')
        print('Estados: ')
        for estado in self.states:
            print(estado.name)
        print('Alfabeto: ')
        for symbol in self.alphabet:
            print(symbol)
        print('Estado inicial: ')
        print(self.start_state.name)
        print('Estados finales: ')
        for state in self.final_states:
            print(state.name)

        print('___________________________')
