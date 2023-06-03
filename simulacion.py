class simulacion:
    def __init__(self, automata, input):
        self.automata = automata
        self.input = input

    def iniciarSimulacion(self):
        value = self.simular()
        if value:
            print('La cadena es valida')
        else:
            print('La cadena no es valida')

    def simular(self):

        checkE = False
        for i in self.automata.states:
            for j in i.transition_to:
                if j.symbol == 'ε':
                    checkE = True
                    break

        current = []
        current.append(self.automata.start_state)
        if checkE:

            epsilon = self.episolon(self.automata.start_state)
            for i in epsilon:
                current.append(i)

        for i in self.input:
            temp = []
            for j in current:
                for statei in self.automata.states:
                    if statei.name == j.name:
                        for transition in statei.transition_to:
                            if transition.symbol == i:
                                temp.append(transition.state)
            if len(temp) == 0:
                return False
            current = temp
            if checkE:
                for i in temp:
                    epsilon = self.episolon(i)
                    for j in epsilon:
                        dontR = self.dontRepeat(j, temp)
                        if dontR == True:
                            temp.append(j)
            if len(temp) > 0:
                current = temp
            else:
                return False

        for i in current:
            for j in self.automata.final_states:
                if i.name == j.name:
                    return True
        return False

    def episolon(self, state):
        closure = []

        for transition in state.transition_to:
            if transition.symbol == 'ε':
                closure.append(transition.state)
                temp = self.episolon(transition.state)
                for stateTemp in temp:
                    closure.append(stateTemp)

        return closure

    def dontRepeat(self, state, stateList):
        for stateTemp in stateList:
            if stateTemp.name == state.name:
                return stateTemp
        return True
