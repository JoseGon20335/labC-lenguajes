
from graph.createGraph import *
from NFA import *
import postfix
from Tree import *
from DFA import *
from yalReader import *
from DFADirect import *
from simulacion import *
from writeFile import *
from results.simulacionArchivo import tokens
from yapalReader import *
from LR0 import *

alfabetoA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε', 'E', 'ϵ']
alfabetoB = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ε', 'E', 'ϵ']
alfabetoC = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
operadores = ['|', '*', '+', '?', '(', ')', '.']
precedence = {'(': 1, '(': 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}


def main():

    yalFile = 'yal/slr-3.yal'
    yapalFile = 'yapar/slr-3.yalp'

    print('___________________________')
    yapalRead = yapalReader(yapalFile)
    yapalInput = yapalRead.startReader()
    print('___________________________')

    print('___________________________')
    yalRead = yalReader(yalFile)
    yalexInput = yalRead.startReader()
    print('___________________________')

    print('___________________________')
    print(yapalInput.tokens)
    print(yapalInput.expresions)
    lr0 = LR0()
    lr0.startLR0(yapalInput.expresions, yapalInput.tokens)
    print('___________________________')


main()
