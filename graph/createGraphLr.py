from graphviz import Digraph
from collections import deque


class createGraphLr(object):

    def __init__(this, data=None, startState=None) -> None:
        this.data = data
        this.startState = startState

    def createGraph(this):
        afdGraph = Digraph('results/lr0', 'resultado')
        afdGraph.graph_attr['rankdir'] = 'LR'
        afdGraph = this.addNodeToGraph(afdGraph, this.data)
        afdGraph.view()

    def addNodeToGraph(this, afdGraph, data):
        states = data
        for state in states:
            if state.symbol == 0:
                afdGraph.node(str(state.name), str(state.name), shape='square')
            elif state.symbol == 1:
                if state.name == this.startState.name:
                    afdGraph.node(str(state.name), str(
                        state.name), shape='square', color='green')
                else:
                    afdGraph.node(str(state.name), str(
                        state.name), shape='square', color='red')
        for state in states:
            if state.transition_to is not None:
                for transition in state.transition_to:
                    afdGraph.edge(str(state.name), str(
                        transition.state.name), transition.symbol)

        return afdGraph
