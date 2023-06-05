class simulacion:
    def __init__(self, automata, nameFile):
        self.automata = automata
        self.input = ''
        self.resultSimulacion = []
        self.nameFile = nameFile

    def iniciarSimulacion(self):
        self.input = self.readTxt()
        myString = []
        tokenWork = ''
        work = ''
        index = 0
        while index < len(self.input):
            i = self.input[index]
            myString.append(str(ord(i)))
            value = self.simular(myString)
            if value == False:
                if work != '':
                    index -= 1
                    self.resultSimulacion.append([work, tokenWork])
                else:
                    symbol_string = ""
                    for ascii_val in myString:
                        symbol_string += chr(int(ascii_val))
                    self.resultSimulacion.append(
                        [symbol_string, 'error sintactico'])
                work = ''
                tokenWork = ''
                myString = []
            else:
                symbol_string = ""
                for ascii_val in myString:
                    symbol_string += chr(int(ascii_val))
                tokenWork = value
                work = symbol_string
            index += 1
        print(self.resultSimulacion)

    def simular(self, inputSim):

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

        for i in inputSim:
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
                    return j.token
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

    def readTxt(self):
        file_path = self.nameFile
        with open(file_path, 'r') as file:
            file_contents = file.read()

        return file_contents
