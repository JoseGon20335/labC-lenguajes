class yalReader:
    def __init__(self, yalName):
        self.yalName = yalName
        self.tokens = {}
        self.goodTokens = []

    def startReader(self):
        self.readTokens()
        print('hola')
        self.asciFicacion()

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

    def asciFicacion(self):  # pense que sonaria como zombificacion pero quedo medio raro XD

        for value1 in self.tokens:
            for value2 in self.tokens:
                if value1 != value2:
                    temp = self.tokens[value2]
                    result = ''
                    de = ''
                    a = ''
                    if temp[0] == '[':
                        flag = 0
                        for possition, letter in enumerate(temp):
                            ascii_code = ord(letter)
                            result = result + ascii_code + '|'
                            # basicamente quiero analizar como separar las comas cuando se refiere de
                            # ['A'-'Z']
                            # porque pueden existir casos donde adentro haya '-'y lo tengo que analizar aparte
