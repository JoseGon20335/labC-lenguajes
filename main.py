
from createGraph import *
from NFA import *
import postfix
from Tree import *


alfabetoA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε', 'E', 'ϵ']
alfabetoB = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ε', 'E', 'ϵ']
operadores = ['|', '*', '+', '?', '(', ')', '.']
precedence = {'(': 1, "(": 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}


def main():

    # expresion = '(a*|b*)c'
    # expresion = '0?(1?)?0*'
    # expresion = 'a(a?b*|c+)b|baa'
    # expresion = '(a*|b*)c'
    # expresion = '(b|b)*abb(a|b)*'
    # expresion = '(a|ε)b(a+)c?'
    # expresion = '(a|b)*a(a|b)(a|b)'
    # expresionInput = input('Ingrese el redex a evaluar. Por ejemplo: a|b')
    # expresion = evaluateInput().evaluate(expresionInput)

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


main()
