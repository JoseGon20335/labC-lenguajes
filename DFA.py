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
        temp.alphabet.sort()  # revisar si hace falta o no
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

    # def minimizedAfd(self, afd):
    #     # Initialize partitions
    #     partitions = [set(afd.final_states), set(
    #         afd.states) - set(afd.final_states)]

    #     # Initialize state mapping
    #     state_mapping = {
    #         state: 0 if state in partitions[0] else 1 for state in afd.states}

    #     # Initialize worklist
    #     worklist = [(0, 1)]

    #     # Hopcroft's algorithm
    #     while worklist:
    #         # Get a pair (P, X) from the worklist
    #         P, X = worklist.pop()

    #         # Split the partitions
    #         for c in afd.alphabet:
    #             P1 = set()
    #             for state in P:
    #                 if afd.transitions.get((state, c), None) is not None:
    #                     P1.add(afd.transitions[(state, c)])
    #             for i, Q in enumerate(partitions):
    #                 if len(Q.intersection(P1)) > 0 and len(Q.difference(P1)) > 0:
    #                     partitions.remove(Q)
    #                     partitions.append(Q.intersection(P1))
    #                     partitions.append(Q.difference(P1))
    #                     for state in Q.intersection(P1):
    #                         state_mapping[state] = len(partitions) - 2
    #                         if state in Q.difference(P1):
    #                             state_mapping[state] = len(partitions) - 1
    #                     for state in Q.difference(P1):
    #                         state_mapping[state] = len(partitions) - 1
    #                     if (i, X) in worklist:
    #                         worklist.remove((i, X))
    #                         worklist.append((len(partitions) - 2, X))
    #                         worklist.append((len(partitions) - 1, X))
    #                     else:
    #                         if len(partitions) - 2 < X:
    #                             worklist.append((len(partitions) - 2, X))
    #                         else:
    #                             worklist.append((X, len(partitions) - 2))
    #                         if len(partitions) - 1 < X:
    #                             worklist.append((len(partitions) - 1, X))
    #                         else:
    #                             worklist.append((X, len(partitions) - 1))

    #     # Create the minimized AFD
    #     minimized_afd = AFD()
    #     minimized_afd.alphabet = afd.alphabet
    #     minimized_afd.initial_state = state_mapping[afd.initial_state]
    #     minimized_afd.final_states = {
    #         state_mapping[state] for state in afd.final_states}
    #     minimized_afd.states = set(range(len(partitions)))
    #     minimized_afd.transitions = {}
    #     for state in afd.states:
    #         for c in afd.alphabet:
    #             if afd.transitions.get((state, c), None) is not None:
    #                 minimized_afd.transitions[(
    #                     state_mapping[state], c)] = state_mapping[afd.transitions[(state, c)]]

    #     return minimized_afd

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
                for state in states:
                    if state not in node.related:
                        break
                    else:
                        return node

        return True
