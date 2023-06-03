
from createGraph import *
from NFA import *
import postfix
from Tree import *
from DFA import *
from DFADirect import *
from simulacion import *

alfabetoA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε', 'E', 'ϵ']
alfabetoB = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ε', 'E', 'ϵ']
alfabetoC = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
operadores = ['|', '*', '+', '?', '(', ')', '.']
precedence = {'(': 1, '(': 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}


def main():
    expresion = '(a*|b*)c'
    # expresion = '0?(1?)?0*'
    # expresion = 'a(a?b*|c+)b|baa'
    # expresion = '(b|b)*abb(a|b)*'
    # expresion = '(a|ε)b(a+)c?'
    # expresion = '(a|b)*a(a|b)(a|b)'
    # expresion = 'a(a?b*|c+)b|baa'
    # expresion = '(a?)'

    # PRIMERO SE PASA A POSTFIX
    print('___________________________')
    print('expresion: ', expresion)
    postFix = postfix.passToPostFix(expresion)
    print('postfix: ', postFix)
    print('___________________________')

    # VAMOS A PASAR EL POSTFIX A UN ARBOL
    tree = Tree(postFix=postFix, nameOfTree='tree')
    tree.postFixToTree()

    print('___________________________')

    # VAMOS A PASAR EL ARBOL A UN NFA
    nfa = NFA(tree=tree.tree)
    nfa.convert()

    print('___________________________')

    # VAMOS A PASAR EL NFA A UN AFD
    dfa = DFA(nfa.afn, alfabetoC)
    dfa.convert()

    print('___________________________')

    # VAMOS A PASAR EL POSTFIX A DFA DIRECTO
    dfaDirecto = DFADirect()
    dfaDirecto.convert(postfix=postFix)

    print('___________________________')
    # # VAMOS A SIMULAR
    print('VAMOS A SIMULAR INGRESE LA CADENA AFN: \n')
    inputSim = input()
    sim = simulacion(nfa.afn, inputSim)
    sim.iniciarSimulacion()

    print('VAMOS A SIMULAR INGRESE LA CADENA AFD: \n')
    inputSim = input()
    sim = simulacion(dfa.afd, inputSim)
    sim.iniciarSimulacion()

    print('VAMOS A SIMULAR INGRESE LA CADENA AFD DIRECTO: \n')
    inputSim = input()
    sim = simulacion(dfaDirecto, inputSim)
    sim.iniciarSimulacion()


main()
