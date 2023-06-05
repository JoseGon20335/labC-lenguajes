
from graph.createGraph import *
from NFA import *
import postfix
from Tree import *
from DFA import *
from yalReader import *
from DFADirect import *

alfabetoA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε', 'E', 'ϵ']
alfabetoB = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ε', 'E', 'ϵ']
alfabetoC = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
operadores = ['|', '*', '+', '?', '(', ')', '.']
precedence = {'(': 1, '(': 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}


def mainC():

    yalFile = 'yal/slr-1.yal'

    yalRead = yalReader(yalFile)
    yalexInput = yalRead.startReader()

    print('___________________________')
    print('expresion: ', yalexInput)
    postFix = postfix.passToPostFix(yalexInput)
    print('postfix: ', postFix)
    print('___________________________')
    print(yalRead.tokens)
    print('___________________________')
    print(yalRead.goodTokens)
    print('___________________________')
    print(yalRead.ruleTokens)
    print('___________________________')
    # VAMOS A PASAR EL POSTFIX A UN ARBOL
    tree = Tree(postFix=postFix, nameOfTree='tree')
    tree.postFixToTree()
    print('___________________________')


mainC()
