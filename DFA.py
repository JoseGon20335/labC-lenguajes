from createGraphAfn import *


class transition:
    def __init__(self, state, symbol):
        self.state = state
        self.symbol = symbol


class NODE:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.related = []

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
        self.afn = self.afn_to_afd(self.afn)
        self.print_result()
        graph = createGraphAfn(data=self.afn)
        graph.createGraph()
        return self.afn

    def afn_to_afd(self, afnInput):

        temp = AFD()
        temp.alphabet = afnInput.alphabet
        temp.alphabet.remove('ε')

        tempEpisolon = self.episolon(afnInput.start_state)
        nameNode = str(self.alfabeto[self.state_counter])
        nodo = NODE(nameNode, 1, tempEpisolon)

        if(nodo.symbol == 2):
            temp.set_final_state(nodo)
            nodo.symbol = 3

        temp.add_state(nodo)
        self.state_counter += 1
        temp.start_state = nodo

        self.expectStates.append(nodo)

        while len(self.expectStates) != 0:
            state = self.expectStates[0]
            self.expectStates.remove(state)

            for symbol in temp.alphabet:

                tempEpisolon = []
                statesSymbol = self.symbol(state.related, symbol)
                addStates = []
                # aqui estoy
                for stateSymbol in statesSymbol:
                    statesEpisolon = self.episolon(stateSymbol)
                    for stateEpisolon in statesEpisolon:
                        addStates.append(stateEpisolon)

                addStates = list(set(addStates))

                for stateEpisolon in state.related:
                    tempEpisolon.append(stateEpisolon)

                for stateEpisolon in state.related:
                    for transition in stateEpisolon.transition_to:
                        if transition.symbol == symbol:
                            tempEpisolon.append(transition.state)

                if len(tempEpisolon) != 0:
                    tempEpisolon = self.episolon(tempEpisolon)
                    nameNode = str(self.alfabeto[self.state_counter])
                    nodo = NODE(nameNode, 1, tempEpisolon)

                    if(nodo.symbol == 2):
                        temp.set_final_state(nodo)
                        nodo.symbol = 3

                    temp.add_state(nodo)
                    state.add_transition(nodo, symbol)
                    self.state_counter += 1
                    self.expectStates.append(nodo)

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

    def episolon(self, state):
        closure = []
        closure.append(state)

        for transition in state.transition_to:
            if transition.symbol == 'ε':
                closure.append(transition.state)
                temp = []
                temp = self.episolon(transition.state)
                for state in temp:
                    closure.append(state)

        return closure

    def symbol(self, states, symbol):
        symbolList = []
        symbolList.append(state)

        for state in states:
            for transition in state.transition_to:
                if transition.symbol == symbol:
                    symbolList.append(transition.state)

        return symbolList
