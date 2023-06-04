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


class LR0:
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
        self.alfabeto = alfabeto
        self.state_counter = 0
        self.expectStates = []

    def startLR0(self):
