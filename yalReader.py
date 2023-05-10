class yalReader:
    def __init__(self, yalName):
        self.yalName = yalName
        self.tokens = {}
        self.goodTokens = []

    def startReader(self):
        self.readTokens()
        print('hola')
        self.readGoodTokens()
        print(self.tokens)

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
                print(words)
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
        respuesta = ''
        for i in result:
            respuesta = respuesta + str(i) + '|'
        self.tokens[key] = respuesta

    def tokenToData(self, temp):
        word = ''
        word2 = ''
        for position, value in enumerate(temp):
            word = word + value
            if(value == "(" or value == ')' or value == '|' or value == '*' or value == '+' or value == '?' or value == '.'):
                word = ''
                word2 = word2 + value
            if word in self.tokens:
                key = word
                word = ''
                for position2, value2 in enumerate(temp):
                    if position < position2:
                        temp2 = self.tokenToData(temp[position2:])
                        word2 = self.tokens[key]
                        word2 = word2 + temp2
                        return word2

        return word2

# leer por aparte
