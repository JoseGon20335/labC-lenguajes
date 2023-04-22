from graphviz import Digraph
from collections import deque


class createGraphAfn(object):

    def __init__(this, data=None) -> None:
        this.data = data

    def createGraph(this):
        afnGraph = Digraph('AFN', 'resultado')
        afnGraph.graph_attr['rankdir'] = 'LR'
        afnGraph = this.addNodeToGraph(afnGraph, this.data)
        print("afnGraph", afnGraph)
        afnGraph.view()

    def addNodeToGraph(this, afnGraph, data):
        print("data", data)  # revisar que onda con la data porque no corresponde
        states = data.states
        for state in states:
            if state.symbol == 0:
                afnGraph.node(str(id(state)), str(state.name), shape='circle')
            elif state.symbol == 1:
                afnGraph.node(str(id(state)), str(state.name), shape='circle')
            elif state.symbol == 2:
                afnGraph.node(str(id(state)), str(
                    state.name), shape='doublecircle')
        # 4 y 8
        for state in states:
            if state.transition_to is not None:
                for transition in state.transition_to:
                    afnGraph.edge(str(id(state)), str(
                        id(transition.state)), transition.symbol)

    # def addNodeToGraph(this, afnGraph, data):
    #     print("data", data)  # revisar que onda con la data porque no corresponde
    #     states = data.states
    #     for state in states:
    #         if state.symbol == 0:
    #             afnGraph.node(str(state.name), str(state.name), shape='circle')
    #         elif state.symbol == 1:
    #             afnGraph.node(str(state.name), str(state.name), shape='circle')
    #         elif state.symbol == 2:
    #             afnGraph.node(str(state.name), str(
    #                 state.name), shape='doublecircle')
    #     # 4 y 8
    #     for state in states:
    #         if state.transition_to is not None:
    #             for transition in state.transition_to:
    #                 afnGraph.edge(str(state.name), str(
    #                     state.name), transition.symbol)

        return afnGraph
