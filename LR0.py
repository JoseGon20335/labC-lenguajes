from graph.createGraphLr import *
from tabulate import tabulate


class transition:
    def __init__(self, state, symbol):
        self.state = state
        self.symbol = symbol


class NODE:
    def __init__(self, name, symbol, productions):
        self.name = name
        self.symbol = symbol
        self.productions = productions
        self.transition_to = []

    def add_transition(self, transition_to, transition_name):
        transitionTemp = transition(transition_to, transition_name)
        self.transition_to.append(transitionTemp)


class LR0:
    def __init__(self, ignores, simulacion, diccionario):
        self.alphabet = []
        self.state_counter = 0
        self.expresions = []
        self.tokens = []
        self.states = []
        self.start_state = None
        self.final_states = []
        self.initial_state = None
        self.testUse = None
        self.tableGoto = [[]]
        self.tableActions = [[]]
        self.ignores = ignores
        self.simulacion = simulacion
        self.diccionario = diccionario

    def startLR0(self, expresions, tokens):
        self.tokens = tokens
        self.testUse = expresions
        self.formateExpresiones(expresions=expresions)
        self.expresions = self.agregarPunto()

        for i in self.expresions:
            checkTerminal = i.split('->')[0]
            if checkTerminal not in self.tokens:

                self.start_state = i
                clousure = self.clousure(i)
                node = NODE(self.stringIficador(clousure), 1, clousure)
                self.initial_state = node
                break

        self.states.append(self.initial_state)

        for state in self.states:
            for symbol in self.alphabet:
                node = self.gatoGoto(state, symbol)
                if node != None:
                    check = True
                    for i in self.states:
                        if i.name == node.name:
                            check = False
                            break
                    if check:
                        self.states.append(node)

                        if node.symbol == 1:
                            self.final_states.append(node)

                    state.add_transition(node, symbol)

        self.funcionesTest()

        graph = createGraphLr(self.states, self.initial_state)
        graph.createGraph()

        self.makeTable()

    def formateExpresiones(self, expresions):
        start = True
        for expresion in expresions:
            self.alphabet.append(expresion)
            if start:
                valueToAdd = expresion + '`' + ' -> ' + expresion
                self.expresions.append(valueToAdd)
                start = False

            getValueExp = expresions[expresion]
            for i in getValueExp:
                valueToAdd = expresion + ' -> ' + i
                self.expresions.append(valueToAdd)
                slitGetValueExp = i.split(' ')
                for j in slitGetValueExp:
                    if j not in self.alphabet:
                        self.alphabet.append(j)
        haveL = []
        for i in self.alphabet:
            if len(haveL) == 0:
                haveL.append(i)
            else:
                if i not in haveL:
                    haveL.append(i)
        self.alphabet = haveL

    def agregarPunto(self):
        result = []
        for expresion in self.expresions:
            expresionSplit = expresion.split('->')
            expresionSplit[1] = ' .' + expresionSplit[1]
            expresion = expresionSplit[0] + '->' + expresionSplit[1]
            result.append(expresion)
        return result

    # go to suena a gato, entonces el gatoGoto :)
    def gatoGoto(self, state, symbol):
        result = []
        for item in state.productions:
            itemSplit = item.split('->')
            itemSplitPunto = [itemSplit[1].split('.')[1].split()][0]
            if len(itemSplitPunto) > 0:
                if itemSplitPunto[0] == symbol:

                    valuesAntes, valueDespues = item.split('.')
                    valueDespues = valueDespues.split()

                    if len(valueDespues) == 1:
                        tempVal = valuesAntes + ' ' + valueDespues[0] + ' .'
                        item = tempVal
                    else:
                        valueDespuesAdd = ''
                        for i in valueDespues[1:]:
                            valueDespuesAdd = valueDespuesAdd + ' ' + i
                        tempVal = valuesAntes + ' ' + \
                            valueDespues[0] + ' .' + valueDespuesAdd
                        item = tempVal
                    result.append(item)

        for item in result:
            itemSplit = item.split('.')[1].split()
            if len(itemSplit) > 0:
                right = itemSplit[0]
                if right not in self.tokens:
                    if right != '->':
                        clousure = self.clousure(item)
                        for i in clousure:
                            if i not in result:
                                result.append(i)

        if len(result) > 0:
            for item in result:
                temp1 = item.replace('.', '').strip()
                temp2 = self.start_state.replace('.', '').strip()
                if temp1 == temp2:
                    right = self.start_state.split('.')[1].split()[0].strip()
                    left = item.split('.')[0].split()[-1].strip()

                    if right == left:
                        node = NODE(self.stringIficador(
                            result), 1, result)
                        return node
                else:
                    node = NODE(self.stringIficador(
                        result), 0, result)
                    return node
        else:
            return None

    def clousure(self, item):
        result = []
        result.append(item)

        for i in result:
            for j in self.expresions:
                iSplit = i.split('->')[1].split('.')[1].split()[0].strip()
                jSplit = j.split('->')[0].strip()
                if iSplit == jSplit:
                    tempVal = j.split('->')
                    tempVal = tempVal[0] + '->' + tempVal[1]

                    if tempVal not in result:
                        result.append(tempVal)

        return result

    def stringIficador(self, productions):
        result = ''
        for i in productions:
            result = result + i + ' \n '
        return result

    def funcionesTest(self):

        for i in self.alphabet:
            print('____________________________________')
            print('First de: ', i)
            print(self.grammaAnaliticsFist(i))
            print('____________________________________')
            print('Follow de: ', i)
            print(self.grammaAnaliticsFollow(i))
            print('____________________________________')

    def grammaAnaliticsFist(self, symbol):
        result = []
        if symbol in self.tokens:
            result.append(symbol)
            return result
        for i in self.testUse[symbol]:
            values = i.split(' ')
            if values[0] in self.tokens:
                if values[0] not in result:
                    result.append(values[0])
            elif values[0] != symbol:
                temp = self.grammaAnaliticsFist(values[0])
                result.extend(temp)
        result = list(set(result))
        return result

    def grammaAnaliticsFollow(self, symbolIn, iteration=0):
        result = []
        symbol = symbolIn.strip()
        if iteration < 100:
            if symbol == list(self.testUse.keys())[0]:
                result.append('DOLLAR')
            for i in self.testUse:
                valueTemp = self.testUse[i]
                for j in valueTemp:
                    if symbol in j:
                        temp = j.split().index(symbol)

                        if temp == len(j.split()) - 1:
                            if i != symbol:
                                temp2 = self.grammaAnaliticsFollow(
                                    i, iteration=iteration + 1)
                                result.extend(temp2)
                        else:
                            jSplit = j.split()
                            valueTemp = self.grammaAnaliticsFist(
                                jSplit[temp + 1])
                            if 'ε' in valueTemp:
                                if i != symbol:
                                    valueTemp2 = self.grammaAnaliticsFollow(
                                        i, iteration=iteration + 1)
                                    result.extend(valueTemp2)
                                valueTemp.remove('&')
                            result.extend(valueTemp)
            result = list(set(result))
            return result
        else:
            return []

    def makeTable(self):
        columnsTerminals = []
        columnsNoTerminals = []
        for i in self.tokens:
            if i not in self.ignores:
                columnsTerminals.append(i)
        columnsTerminals.append('DOLLAR')
        for i in self.alphabet:
            if i not in self.tokens:
                columnsNoTerminals.append(i)
        print(columnsTerminals)
        print(columnsNoTerminals)

        self.tableGoto = [[None] * len(columnsNoTerminals)
                          for _ in range(len(self.states))]

        for i in self.states:
            for j in i.transition_to:
                if j.symbol in columnsNoTerminals:
                    self.tableGoto[self.buscarEstadoPorNombre(
                        i.name)][columnsNoTerminals.index(j.symbol)] = self.buscarEstadoPorNombre(j.state.name)

        self.tableActions = [[None] * len(columnsTerminals)
                             for _ in range(len(self.states))]

        for i in self.states:
            for j in i.transition_to:
                if j.symbol in columnsTerminals:
                    valueTemp = self.tableActions[self.buscarEstadoPorNombre(
                        i.name)][columnsTerminals.index(j.symbol)]
                    if valueTemp == None:
                        self.tableActions[self.buscarEstadoPorNombre(
                            i.name)][columnsTerminals.index(j.symbol)] = "S" + str(self.buscarEstadoPorNombre(j.state.name))
                    else:
                        raise Exception('Error: No es SLR')

        for i in self.states:
            for j in i.productions:
                if j.split('->')[1].split('.')[1].split() == []:
                    if j.split('->')[0] == self.start_state.split('->')[0]:
                        valueTemp = self.tableActions[self.buscarEstadoPorNombre(
                            i.name)][columnsTerminals.index('DOLLAR')]
                        if valueTemp == None:
                            self.tableActions[self.buscarEstadoPorNombre(
                                i.name)][columnsTerminals.index('DOLLAR')] = 'ACEPTENCE'
                        else:
                            raise Exception(
                                'Conflict ', self.buscarEstadoPorNombre(i.name), ', ', k, ' = ', valueTemp)
        for i in self.states:
            for j in i.productions:
                if j.split('->')[1].split('.')[1].split() == []:
                    if j.split('->')[0] != self.start_state.split('->')[0]:
                        followValues = self.grammaAnaliticsFollow(
                            j.split('->')[0])
                        for k in followValues:
                            if k in columnsTerminals:
                                valueTemp = self.tableActions[self.buscarEstadoPorNombre(
                                    i.name)][columnsTerminals.index(k)]
                                if valueTemp == None:
                                    self.tableActions[self.buscarEstadoPorNombre(
                                        i.name)][columnsTerminals.index(k)] = 'R' + str(self.buscarEstadoSinPunto(j))
                                else:
                                    raise Exception(
                                        'Conflict: ' + str(self.buscarEstadoPorNombre(i.name)) + ', ' + str(k) + ' = ' + valueTemp + ', R' + str(self.buscarEstadoSinPunto(j)))
        # print('go to')
        # for i in self.tableGoto:
        #     print(i)
        # print('_________________________________________________________')
        # print('action')
        # for i in self.tableActions:
        #     print(i)

        print('Action Table:')
        print(tabulate(self.tableActions, headers=range(
            len(self.tableActions[0])), tablefmt='grid'))

        print('\nGoto Table:')
        print(tabulate(self.tableGoto, headers=range(
            len(self.tableGoto[0])), tablefmt='grid'))

        print('_________________________________________________________')

        resultTemp = []
        for j in self.simulacion.resultSimulacion:
            value = self.returnReturnable(j[1])
            if value != None:
                if value.replace(' ', '').replace('return', '') not in self.ignores:
                    resultTemp.append(value.replace(
                        ' ', '').replace('return', ''))
                    continue

        print(resultTemp)
        print('_________________________________________________________')

        self.parse(resultTemp, columnsTerminals, columnsNoTerminals)

        print('_________________________________________________________')

        print('dale Zelda dale')

    def buscarEstadoPorNombre(self, nombre):
        for i in range(len(self.states)):
            state = self.states[i]
            if state.name == nombre:
                return i
        return None

    def buscarEstadoSinPunto(self, nombre2):
        nombre = nombre2.replace('.', '').strip().replace(' ', '')
        for i in range(len(self.initial_state.productions)):
            state = self.initial_state.productions[i]
            if state.replace('.', '').strip().replace(' ', '') == nombre:
                return i

    def parse(self, input_string, listTerminals, listNoTerminals):
        # Initialize the stack with the initial state
        stack = [self.initial_state]
        input_tokens = input_string
        input_tokens.append('DOLLAR')  # Add end-of-input marker
        listTerminals.append('$')
        output = []

        while True:
            current_token = input_tokens[0]
            state = stack[-1]  # Get the top of the stack without popping it
            action = self.tableActions[self.buscarEstadoPorNombre(
                state.name)][listTerminals.index(current_token)]

            if action is None:
                print("Error: Invalid input at position", len(output))
                return False

            if action.startswith("S"):
                next_state = int(action[1:])
                stack.append(self.states[next_state])
                output.append(current_token)
                input_tokens.pop(0)
            elif action.startswith("R"):
                next_state = int(action[1:])
                production = self.initial_state.productions[next_state]
                left, right = production.split("->")
                left = left.strip()
                rightTemp = right.strip().replace('.', '').split()

                for i in rightTemp:
                    if i == '':
                        rightTemp.remove(i)
                for _ in range(len(rightTemp)):
                    stack.pop()

                # Get the top of the stack without popping it
                top_state = stack[-1]
                next_state = self.tableGoto[self.buscarEstadoPorNombre(
                    top_state.name)][listNoTerminals.index(left)]

                stack.append(self.states[next_state])

            elif action == "ACEPTENCE":
                print("Input accepted.")
                return True
            else:
                print("Error: Invalid input at position", len(output))
                return False

        return output

    def returnReturnable(self, string):
        string = string.replace('#', '')
        key = ''
        for i in self.diccionario:
            check = self.is_convertible_to_int(i)
            if check:
                key = chr(int(i))
            else:
                key = i
            if key == string:
                return self.diccionario[i]

    def is_convertible_to_int(self, string):
        return string.isdigit()
