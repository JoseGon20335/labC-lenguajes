
from graph.createGraph import *
from NFA import *
import postfix
from Tree import *
from DFA import *
from yalReader import *


alfabetoA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε', 'E', 'ϵ']
alfabetoB = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ε', 'E', 'ϵ']
alfabetoC = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
operadores = ['|', '*', '+', '?', '(', ')', '.']
precedence = {'(': 1, '(': 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}


def mainAyB():
    pasar = True
    expresion = ''
    # while pasar:
    #     print('Ingrese la expresion regular:')
    #     expresion = input()
    #     if expresion == '':
    #         print('Expresion regular vacia.')
    #     elif expresion == ' ':
    #         print('Expresion regular vacia.')
    #     else:
    #         pasar = False

    # expresion = '(a*|b*)c'
    # expresion = '0?(1?)?0*'
    # expresion = 'a(a?b*|c+)b|baa'
    # expresion = '(a*|b*)c'
    # expresion = '(b|b)*abb(a|b)*'
    # expresion = '(a|ε)b(a+)c?'
    # expresion = '(a|b)*a(a|b)(a|b)'
    # expresionInput = input('Ingrese el redex a evaluar. Por ejemplo: a|b')
    # expresion = evaluateInput().evaluate(expresionInput)
    # expresion = 'a(a?b*|c+)b|baa'
    # expresion = '(a?)'

    # PRIMERO SE PASA A POSTFIX
    print('___________________________')
    print('expresion: ', expresion)
    postFix = postfix.passToPostFix(expresion)
    print('postfix: ', postFix)
    print('___________________________')

    # VAMOS A PASAR EL POSTFIX A UN ARBOL
    tree = Tree(postFix=postFix)
    tree.postFixToTree()

    # VAMOS A PASAR EL ARBOL A UN NFA
    nfa = NFA(tree=tree.tree)
    nfa.convert()

    # VAMOS A PASAR EL NFA A UN AFD
    dfa = DFA(afn=nfa.afn, alfabeto=alfabetoC)
    dfa.convert()


def mainC():

    yalFile = 'yal/slr-1.yal'

    yalRead = yalReader(yalFile)
    yalRead.startReader()


# mainAyB()
mainC()
