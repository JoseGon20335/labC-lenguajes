
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

    yalFile = 'prueba/lab-f.yal'
    yapalFile = 'prueba/lab-f.yalp'
    # yalFile = 'prueba/lab-f.yal'
    # yapalFile = 'prueba/lab-f.yalp'

    print('READER YAL___________________________')
    yalRead = yalReader(yalFile)
    yalexInput = yalRead.startReader()
    print('END READ YAL_________________________')
    print('POSTFIX______________________________')
    post = postfix.passToPostFix(yalexInput)
    print('END POSTFIX__________________________')
    print('TREE DFA_____________________________')
    dfa = DFADirect()
    dfa.convert(post)
    print('END TREE DFA_________________________')
    print('SIMULACION___________________________')
    sim = simulacion(dfa, 'prueba/prueba3F.txt')
    sim.iniciarSimulacion()
    print('END SIMULACION_______________________')
    print('READ YAPAL___________________________')
    yapalRead = yapalReader(yapalFile)
    yapalInput = yapalRead.startReader()
    print('END READ YAPAL_______________________')
    print('MAKE SLR_____________________________')
    lr0 = LR0(ignores=yapalInput.ignores, simulacion=sim,
              diccionario=yalRead.goodTokens)
    lr0.startLR0(yapalInput.expresions, yapalInput.tokens)
    print('END MAKE SLR_________________________')


main()
