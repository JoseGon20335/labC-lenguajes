from graph.createGraphLr import *


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
    def __init__(self):
        self.alphabet = []
        self.state_counter = 0
        self.expresions = []
        self.tokens = []
        self.states = []
        self.start_state = None
        self.final_states = []
        self.initial_state = None
        self.testUse = None

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

    def grammaAnaliticsFollow(self, symbol):
        result = []
        if symbol == list(self.testUse.keys())[0]:
            result.append('$')
        for i in self.testUse:
            valueTemp = self.testUse[i]
            for j in valueTemp:
                if symbol in j:
                    temp = j.split().index(symbol)

                    if temp == len(j.split()) - 1:
                        if i != symbol:
                            temp2 = self.grammaAnaliticsFollow(i)
                            result.extend(temp2)
                    else:
                        jSplit = j.split()
                        valueTemp = self.grammaAnaliticsFist(
                            jSplit[temp + 1])
                        if 'ε' in valueTemp:
                            if i != symbol:
                                valueTemp2 = self.grammaAnaliticsFollow(i)
                                result.extend(valueTemp2)
                            valueTemp.remove('&')
                        result.extend(valueTemp)
        result = list(set(result))
        return result
