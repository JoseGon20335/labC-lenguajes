
class writeFile:
    def __init__(self, fileName):
        self.fileName = fileName

    def write(self, yalReader):
        with open('./results/' + self.fileName + '.py', 'w') as f:
            f.write('def tokens(listaTokens):\n')
            f.write('\tfor tokenValue in listaTokens:\n')
            f.write('\t\ttoken = tokenValue[1].replace("#","")\n')
            conta = 0
            for i in yalReader:
                if conta == 0:
                    f.write('\t\tif token == "' + i + '":\n')
                    if yalReader[i] == '':
                        f.write('\t\t\treturn None\n')
                    else:
                        f.write('\t\t\t' + yalReader[i] + '\n')
                else:
                    f.write('\t\telif token == "' + i + '":\n')
                    if yalReader[i] == '':
                        f.write('\t\t\treturn None\n')
                    else:
                        f.write('\t\t\t' + yalReader[i] + '\n')
                conta += 1
            f.write('\t\telse: \n\t\t\tprint(' + '"error de sintaxis"' + ')')
