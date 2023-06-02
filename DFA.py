from graph.createGraphAfd import *


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

    def add_transition(self, transition_to, transition_name):
        transitionTemp = transition(transition_to, transition_name)
        self.transition_to.append(transitionTemp)


class AFD:
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


class DFA:
    def __init__(self, afn, alfabeto):
        self.afn = afn
        self.afd = AFD()
        self.alfabeto = alfabeto
        self.state_counter = 0
        self.expectStates = []

    def convert(self):
        self.afd = self.afn_to_afd(self.afn)
        self.print_result()
        graph = createGraphAfd(data=self.afd)
        graph.createGraph()
        return self.afd

    def afn_to_afd(self, afnInput):

        temp = AFD()
        temp.alphabet = afnInput.alphabet
        temp.alphabet.sort()
        if 'ε' in temp.alphabet:
            temp.alphabet.remove('ε')
        tempEpisolon = self.episolon(afnInput.start_state)
        tempEpisolon.append(afnInput.start_state)
        tempEpisolon = list(set(tempEpisolon))
        nameNode = str(self.alfabeto[self.state_counter])
        nodo = NODE(nameNode, 1, tempEpisolon)

        if(nodo.symbol == 2):
            temp.set_final_state(nodo)
            nodo.symbol = 3

        temp.add_state(nodo)
        self.state_counter += 1
        temp.start_state = nodo

        self.expectStates.append(tempEpisolon)

        while len(self.expectStates) != 0:
            state = self.expectStates.pop()

            for symbol in temp.alphabet:
                tempEpisolon = []
                statesSymbol = self.symbolGet(state, symbol)
                addStates = []

                for stateSymbol in statesSymbol:
                    statesEpisolon = self.episolon(stateSymbol)
                    statesEpisolon.append(stateSymbol)
                    statesEpisolon = list(set(statesEpisolon))
                    for stateEpisolon in statesEpisolon:
                        addStates.append(stateEpisolon)

                addStates = list(set(addStates))

                if len(addStates) != 0:
                    # 23 y 18 / b
                    tempChecker = self.dontRepeat(addStates, temp)
                    if tempChecker == True:

                        for stateAdd in addStates:
                            if stateAdd.symbol == 2:
                                nodo = NODE(
                                    self.alfabeto[self.state_counter], 2, addStates)
                                temp.set_final_state(nodo)
                                break
                            else:
                                nodo = NODE(
                                    self.alfabeto[self.state_counter], 1, addStates)

                        temp.add_state(nodo)
                        self.state_counter += 1

                        self.expectStates.append(nodo.related)
                        # error
                        tempRepeat = self.dontRepeat(state, temp)
                        check = True
                        if tempRepeat != True:
                            for stateTemp in temp.states:
                                if stateTemp.name == tempRepeat.name:
                                    for stateTempTransition in stateTemp.transition_to:
                                        if stateTempTransition.symbol == symbol and stateTempTransition.state.name == nodo.name:
                                            check = False

                        if check:
                            for stateTemp in temp.states:
                                if tempRepeat != True:
                                    if stateTemp.name == tempRepeat.name:
                                        stateTemp.add_transition(nodo, symbol)
                    else:
                        tempRepeat = self.dontRepeat(state, temp)
                        tempRepeat2 = self.dontRepeat(addStates, temp)
                        check = True
                        if tempRepeat != True:
                            for stateTemp in temp.states:
                                if stateTemp.name == tempRepeat.name:
                                    for stateTempTransition in stateTemp.transition_to:
                                        if stateTempTransition.symbol == symbol and stateTempTransition.state.name == tempRepeat2.name:
                                            check = False

                        if check:
                            for stateTemp in temp.states:
                                if tempRepeat != True:
                                    if stateTemp.name == tempRepeat.name:
                                        stateTemp.add_transition(
                                            tempRepeat2, symbol)

        return temp

    def print_result(self):
        print('____________AFD____________')
        print('Estados: ')
        for estado in self.afd.states:
            print(estado.name)
        print('Alfabeto: ')
        for symbol in self.afd.alphabet:
            print(symbol)
        print('Estado inicial: ')
        print(self.afd.start_state.name)
        print('Estados finales: ')
        for state in self.afd.final_states:
            print(state.name)

        print('___________________________')

    def episolon(self, state):
        closure = []

        for transition in state.transition_to:
            if transition.symbol == 'ε':
                closure.append(transition.state)
                temp = self.episolon(transition.state)
                for stateTemp in temp:
                    closure.append(stateTemp)

        return closure

    def symbolGet(self, states, symbol):
        symbolList = []
        for state in states:
            for transition in state.transition_to:
                if transition.symbol == symbol:
                    symbolList.append(transition.state)

        return symbolList

    def dontRepeat(self, states, afdActual):
        for node in afdActual.states:
            if len(node.related) == len(states):
                temp = 0
                for state in states:
                    if state in node.related:
                        temp = temp + 1
                if temp == len(states):
                    return node
        return True

    def check_lists_equal(list1, list2):
        check = []
        for element in list1:
            if element not in list2:
                check
