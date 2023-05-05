from graph.createGraphAfn import *


class transition:
    def __init__(self, state, symbol):
        self.state = state
        self.symbol = symbol


class NODE:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.transition_to = []

    def add_transition(self, transition_to, transition_name):
        transitionTemp = transition(transition_to, transition_name)
        self.transition_to.append(transitionTemp)


class AFN:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.start_state = None
        self.final_states = []

    def add_state(self, state):
        self.states.append(state)

    def add_alphabet(self, symbol):
        self.alphabet.append(symbol)

    def set_final_state(self, state):
        self.final_states.append(state)

    def set_super_final_state(self, state):
        self.final_states = [state]

    def get_new_states(self, new_states):
        update_states = []
        if len(self.states) != 0:
            for state in self.states:
                update_states.append(state)
        for state in new_states:
            update_states.append(state)
        self.states = update_states

    def get_new_symbol(self, new_symbol):
        update_symbol = []
        if len(self.alphabet) != 0:
            for symbol in self.alphabet:
                update_symbol.append(symbol)
        for symbol in new_symbol:
            update_symbol.append(symbol)
        self.alphabet = update_symbol


class NFA:
    def __init__(self, tree):
        self.tree = tree
        self.afn = AFN()
        self.state_counter = 0

    def clean_afn(self):
        self.afn.alphabet = list(set(self.afn.alphabet))
        self.afn.final_states = self.afn.set_super_final_state(
            self.afn.final_states[-1])
        # bubble sort algorithm to sort values in ascending order

        for stateCompare in self.afn.states:
            for statesActual in self.afn.states:
                if stateCompare.name == statesActual.name:
                    if stateCompare != statesActual:
                        if len(statesActual.transition_to) == 0:
                            self.afn.states.remove(statesActual)

        for state in self.afn.states:
            for transition in state.transition_to:
                for stateCompare in self.afn.states:
                    if transition.state.name == stateCompare.name:
                        if transition.state != stateCompare:
                            transition.state = stateCompare
        startNumber = self.afn.states[0].name
        finalNumber = self.afn.states[0].name
        for i in range(len(self.afn.states)):
            for j in range(len(self.afn.states)):
                if self.afn.states[i].name < self.afn.states[j].name:
                    if self.afn.states[i].name < startNumber:
                        startNumber = self.afn.states[i].name

        for i in range(len(self.afn.states)):
            if self.afn.states[i].name == startNumber:
                self.afn.states[i].symbol = 1
                self.afn.start_state = self.afn.states[i]

        for i in range(len(self.afn.states)):
            for j in range(len(self.afn.states)):
                if self.afn.states[i].name > self.afn.states[j].name:
                    if self.afn.states[i].name > finalNumber:
                        finalNumber = self.afn.states[i].name

        for i in range(len(self.afn.states)):
            if self.afn.states[i].name == finalNumber:
                self.afn.states[i].symbol = 2
                self.afn.set_super_final_state(self.afn.states[i])

    def convert(self):
        self.afn = self.tree_to_afn(self.tree)
        self.clean_afn()
        self.print_result()
        graph = createGraphAfn(data=self.afn)
        graph.createGraph()
        return self.afn

    def tree_to_afn(self, node):
        if node.leftLeaf is None and node.rightLeaf is None:
            temp = AFN()
            nodeObj = NODE(self.state_counter, 0)
            temp.start_state = nodeObj
            temp.add_state(nodeObj)

            nodeObj2 = NODE(self.state_counter + 1, 0)
            self.state_counter += 1
            temp.add_state(nodeObj2)
            nodeObj.add_transition(nodeObj2, node.name)
            temp.set_super_final_state(nodeObj2)
            temp.add_alphabet(node.name)

            return temp

        elif node.name == '*':  # listo
            temp = AFN()

            nodeObj = NODE(self.state_counter, 0)
            temp.start_state = nodeObj
            self.state_counter += 1
            temp.add_state(nodeObj)

            left = self.tree_to_afn(node.leftLeaf)
            nodeObj.add_transition(left.start_state, 'ε')

            nodeObj2 = NODE(self.state_counter + 1, 0)
            self.state_counter += 1
            temp.add_state(nodeObj2)
            temp.set_super_final_state(nodeObj2)

            nodeObj.add_transition(nodeObj2, 'ε')
            left.final_states[-1].add_transition(nodeObj2, 'ε')
            left.final_states[-1].add_transition(left.start_state, 'ε')
            temp.add_alphabet('ε')
            temp.get_new_states(left.states)
            temp.get_new_symbol(left.alphabet)
            return temp

        elif node.name == '.':  # listo
            temp = AFN()

            nodeObj = NODE(self.state_counter, 0)
            temp.start_state = nodeObj
            temp.add_state(nodeObj)

            left = self.tree_to_afn(node.leftLeaf)
            right = self.tree_to_afn(node.rightLeaf)

            temp.set_super_final_state(right.final_states[-1])

            temp.get_new_states(left.states)
            temp.get_new_states(right.states)
            temp.get_new_symbol(left.alphabet)
            temp.get_new_symbol(right.alphabet)

            return temp

        elif node.name == '|':  # listo
            temp = AFN()

            nodeObj = NODE(self.state_counter, 0)
            temp.start_state = nodeObj
            self.state_counter += 1
            temp.add_state(nodeObj)

            left = self.tree_to_afn(node.leftLeaf)
            nodeObj.add_transition(left.start_state, 'ε')
            self.state_counter += 1

            right = self.tree_to_afn(node.rightLeaf)
            nodeObj.add_transition(right.start_state, 'ε')

            nodeObj2 = NODE(self.state_counter + 1, 0)
            self.state_counter += 1
            temp.set_super_final_state(nodeObj2)
            temp.add_state(nodeObj2)

            left.final_states[-1].add_transition(nodeObj2, 'ε')
            right.final_states[-1].add_transition(nodeObj2, 'ε')

            temp.get_new_states(left.states)
            temp.get_new_states(right.states)
            temp.get_new_symbol(left.alphabet)
            temp.get_new_symbol(right.alphabet)
            return temp

        elif node.name == '?':  # listo
            temp = AFN()

            nodeObj = NODE(self.state_counter, 0)
            temp.start_state = nodeObj
            self.state_counter += 1
            temp.add_state(nodeObj)

            left = self.tree_to_afn(node.leftLeaf)
            nodeObj.add_transition(left.start_state, 'ε')

            nodeObj2 = NODE(self.state_counter + 1, 0)
            self.state_counter += 1
            temp.add_state(nodeObj2)

            nodeObj.add_transition(nodeObj2, 'ε')

            nodeObj3 = NODE(self.state_counter + 1, 0)
            self.state_counter += 1
            temp.add_state(nodeObj3)
            nodeObj2.add_transition(nodeObj3, 'ε')

            nodeObj4 = NODE(self.state_counter + 1, 0)
            self.state_counter += 1
            temp.add_state(nodeObj4)
            temp.set_super_final_state(nodeObj4)
            nodeObj3.add_transition(nodeObj4, 'ε')
            left.final_states[-1].add_transition(nodeObj4, 'ε')
            left.set_super_final_state(nodeObj4)

            temp.get_new_states(left.states)
            temp.get_new_symbol(left.alphabet)

            return temp

        elif node.name == '+':  # listo
            temp = AFN()

            nodeObj = NODE(self.state_counter, 0)
            temp.start_state = nodeObj
            temp.add_state(nodeObj)

            nodeObj2 = NODE(self.state_counter + 1, 0)
            self.state_counter += 2
            temp.add_state(nodeObj2)

            nodeObj.add_transition(nodeObj2, node.leftLeaf.name)
            temp.add_alphabet(node.leftLeaf.name)

            left = self.tree_to_afn(node.leftLeaf)
            nodeObj2.add_transition(left.start_state, 'ε')

            nodeObj3 = NODE(self.state_counter + 1, 0)
            self.state_counter += 1
            temp.add_state(nodeObj3)
            temp.set_super_final_state(nodeObj3)

            nodeObj2.add_transition(nodeObj3, 'ε')
            left.final_states[-1].add_transition(nodeObj3, 'ε')
            left.final_states[-1].add_transition(left.start_state, 'ε')

            symbolTemp = ['ε']
            temp.get_new_states(left.states)
            temp.get_new_symbol(symbolTemp)
            temp.alphabet = self.get_new_symbol
            return temp

    def print_result(self):
        print('____________AFN____________')
        print('Estados: ')
        for state in self.afn.states:
            print(state.name)
        print('Alfabeto: ')
        for symbol in self.afn.alphabet:
            print(symbol)
        print('Estado inicial: ')
        print(self.afn.start_state.name)
        print('Estados finales: ')
        for state in self.afn.final_states:
            print(state.name)

        print('___________________________')
