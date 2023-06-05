class yalReader:
    def __init__(self, yalName):
        self.yalName = yalName
        self.tokens = {}
        self.goodTokens = {}
        self.ruleTokens = ''

    def startReader(self):
        self.readTokens()
        self.readGoodTokens()
        print(self.tokens)
        self.passRules()
        print(self.goodTokens)
        return self.ruleTokens

    def readTokens(self):
        # Open the file for reading
        with open(self.yalName, "r") as file:
            # Loop over each line in the file
            for line in file:
                words = []
                commilas = False
                word = ''
                for char in line:
                    if char == "'":
                        commilas = True

                    if char != ' ' or commilas:
                        word = word + char
                    else:
                        words.append(word)
                        word = ''
                words.append(word)
                for position, word in enumerate(words):
                    if word == 'let':
                        temp = words[position + 3]
                        temp = temp[:-1:]
                        self.tokens[words[position + 1]] = temp

    def readGoodTokens(self):
        for value in self.tokens:
            temp = self.tokens[value]
            if temp[0] == '[':
                self.asciFicacion(temp, value)
                continue
            else:
                self.tokens[value] = self.tokenToData(temp)
                continue

    # pense que sonaria como zombificacion pero quedo medio raro XD
    def asciFicacion(self, temp, key):
        result = []
        flag = 0
        for possition, letter in enumerate(temp):
            if flag == 2:
                if letter == '-':
                    flag += 1
                else:
                    flag = 1
            elif letter == "'" or letter == '"':
                flag += 1
            elif flag == 1:
                result.append(ord(letter))
            elif flag == 4:
                flag = -1
                de = result.pop()
                a = ord(letter)
                for i in range(de, a + 1):
                    result.append(i)
        respuesta = '('
        checker = False
        for i in result:
            if(i == 92):
                checker = True
                continue
            if checker:
                if(i == 116):
                    i = 9
                elif(i == 110):
                    i = 10
                elif(i == 115):
                    i = 32
                checker = False

            respuesta = respuesta + str(i) + '|'

        respuesta = respuesta[:-1:]
        respuesta = respuesta + ')'
        self.tokens[key] = respuesta

    def asciFicacionReturn(self, temp):
        result = []
        replace = []
        flag = 0
        for possition, letter in enumerate(temp):
            replace.append(letter)
            if letter == ']':
                break
            if flag == 2:
                if letter == '-':
                    flag += 1
                else:
                    flag = 1
            elif letter == "'" or letter == '"':
                flag += 1
            elif flag == 1:
                result.append(ord(letter))
            elif flag == 4:
                flag = -1
                de = result.pop()
                a = ord(letter)
                for i in range(de, a + 1):
                    result.append(i)
        checker = False
        respuesta = '('
        respuesta2 = ''
        for i in result:
            if(i == 92):
                checker = True
                continue
            if checker:
                if(i == 116):
                    i = 9
                elif(i == 110):
                    i = 10
                elif(i == 115):
                    i = 32
                checker = False

            respuesta = respuesta + str(i) + '|'
        respuesta = respuesta[:-1]
        respuesta = respuesta + ')'
        for i in replace:
            respuesta2 = respuesta2 + i
        return [respuesta, respuesta2]

    def tokenToData(self, temp):
        word = ''
        word2 = ''
        isLonger = False
        comillas = False
        for position, value in enumerate(temp):
            word = word + value
            if comillas:
                yaestasfeliz = word
                word2 = word2 + str(ord(yaestasfeliz))
                temp2 = self.tokenToData(temp[position + 2:])
                word2 = word2 + temp2
                return word2
            if(value == "(" or value == ')' or value == '|' or value == '*' or value == '+' or value == '?' or value == '.' or value == '[' or value == ']' or value == "'" or value == '"'):
                if value == '[':
                    primerCorchete = temp.find('[')
                    ultimoCorchete = temp.find(']')
                    send = temp[primerCorchete + 1:ultimoCorchete + 1]
                    recibe = self.asciFicacionReturn(send)
                    word2 = word2 + recibe[0]
                    temp2 = self.tokenToData(temp[ultimoCorchete + 1:])
                    word2 = word2 + temp2
                    word = ''
                    return word2
                elif value == "'" or value == '"' or comillas:
                    if comillas:
                        comillas = False
                    else:
                        comillas = True
                else:
                    word2 = word2 + word
                word = ''
            if word in self.tokens:
                checkLonger = self.checkIsLonger(word, temp[position + 1:])
                if checkLonger != True:
                    word = checkLonger
                    isLonger = True
                key = word
                word = ''
                for position2, value2 in enumerate(temp):
                    if isLonger:
                        if position < position2:
                            temp2 = self.tokenToData(temp[position2 + 1:])
                            word2 = word2 + self.tokens[key]
                            word2 = word2 + temp2
                            return word2
                    else:
                        if position < position2:
                            temp2 = self.tokenToData(temp[position2:])
                            word2 = word2 + self.tokens[key]
                            word2 = word2 + temp2
                            return word2
        return word2

    def checkIsLonger(self, word, search):
        result = word
        for i in search:
            result = result + i
            if result in self.tokens:
                return result
        return True

    def passRules(self):
        self.ruleTokens = ''
        startRead = False
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

                returnTemp = False
                tokenTemp = ''
                for position, word in enumerate(words):
                    # esto va a tronar por que cuando quiera buscar el 1 o 2 no va a encontrar nada al final y morira
                    if words[0] == 'rule' and words[1] == 'tokens' and words[2] == '=':
                        startRead = True
                        continue
                    if word == '(*':
                        startRead = False
                    elif word == '*)':
                        startRead = True

                    if startRead:
                        if word in self.tokens and not returnTemp:
                            self.ruleTokens = self.ruleTokens + \
                                self.tokens[word]
                            self.ruleTokens = self.ruleTokens + '."#' + word + '"'
                            tokenTemp = word
                        elif word.startswith("'") and word.endswith("'"):
                            self.ruleTokens = self.ruleTokens + \
                                str(ord(word[1:-1:]))
                            self.ruleTokens = self.ruleTokens + \
                                '."#' + word[1:-1:] + '"'
                            tokenTemp = str(ord(word[1:-1:]))
                        elif word == '|':
                            self.ruleTokens = self.ruleTokens + '|'

                        if word == '{':
                            returnTemp = True
                        elif returnTemp:
                            if word == '}':
                                returnTemp = False
                                startRead = True
                            else:
                                if self.goodTokens.get(tokenTemp) != None:
                                    temp = self.goodTokens[tokenTemp]
                                    self.goodTokens[tokenTemp] = temp + \
                                        ' ' + word
                                else:
                                    self.goodTokens[tokenTemp] = word
