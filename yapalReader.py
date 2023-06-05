class yapalReader:
    def __init__(self, yalName):
        self.yalName = yalName
        self.tokens = []
        self.expresions = {}
        self.ignores = []

    def startReader(self):
        self.readTokens()
        print('terminar')
        return self

    def readTokens(self):
        self.ruleTokens = ''
        startRead = False
        finishTokens = False
        savingExpresion = False
        wordExpresionSave = ''

        # Open the file for reading
        with open(self.yalName, "r") as file:
            # Loop over each line in the file
            for line in file:
                words = []
                word = ''
                for char in line:

                    if char != ' ':
                        word = word + char
                    else:
                        if word == '':
                            continue
                        if word.endswith('\n'):
                            word = word.rstrip("\n")
                            words.append(word)
                        else:
                            words.append(word)
                        word = ''
                if word.endswith('\n'):
                    word = word.rstrip("\n")
                    if word != '':
                        words.append(word)
                else:
                    words.append(word)

                readLine = True
                for position, word in enumerate(words):
                    if word == '/*':
                        startRead = False
                        continue
                    elif word == '*/':
                        startRead = True
                        continue

                    if startRead:
                        if finishTokens == False:
                            if word == '%%':
                                finishTokens = True
                            elif word[0] == '%':
                                es = word[1:]
                                if es == 'token':
                                    rest_of_list = words[position + 1:]
                                    print(rest_of_list)
                                    for i in rest_of_list:
                                        self.tokens.append(i)
                            elif word == 'IGNORE':
                                self.ignores.append(words[position + 1])

                        else:
                            if savingExpresion:
                                if word == ';':
                                    savingExpresion = False
                                elif word == '|':
                                    continue
                                else:
                                    if readLine:
                                        rest_of_list = words[position:]
                                        tempToAdd = ''
                                        for i in rest_of_list:
                                            tempToAdd = tempToAdd + i + ' '
                                        tempToAdd = tempToAdd[:-1]
                                        self.expresions[wordExpresionSave].append(
                                            tempToAdd)
                                        readLine = False
                            else:
                                valueIAdd = word.replace(':', '')
                                self.expresions[valueIAdd] = []
                                wordExpresionSave = valueIAdd
                                savingExpresion = True
