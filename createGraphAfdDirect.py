from graphviz import Digraph
from collections import deque


class createGraphAfdDirect(object):

    def __init__(this, data=None) -> None:
        this.data = data

    def createGraph(this):
        afdGraph = Digraph('results/AFD Directo', 'resultado')
        afdGraph.graph_attr['rankdir'] = 'LR'
        afdGraph = this.addNodeToGraph(afdGraph, this.data)
        afdGraph.view()

    def addNodeToGraph(this, afdGraph, data):
        states = data.states
        for state in states:
            if state.symbol == 0:
                afdGraph.node(str(id(state)), str(state.name), shape='circle')
            elif state.symbol == 2:
                afdGraph.node(str(id(state)), str(state.name), shape='circle')
            elif state.symbol == 1:
                afdGraph.node(str(id(state)), str(
                    state.name), shape='doublecircle')
            elif state.symbol == 3:
                afdGraph.node(str(id(state)), str(
                    state.name), shape='doublecircle')
        for state in states:
            if state.transition_to is not None:
                for transition in state.transition_to:
                    afdGraph.edge(str(id(state)), str(
                        id(transition.state)), transition.symbol)

        return afdGraph
