class AFN:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = dict()
        self.start_state = None
        self.final_states = set()

    def add_state(self, state):
        self.states.add(state)

    def add_alphabet(self, symbol):
        self.alphabet.add(symbol)

    def add_transition(self, state_from, symbol, state_to):
        if state_from not in self.transitions:
            self.transitions[state_from] = dict()
        if symbol not in self.transitions[state_from]:
            self.transitions[state_from][symbol] = set()
        self.transitions[state_from][symbol].add(state_to)

    def set_start_state(self, state):
        self.start_state = state

    def set_final_state(self, state):
        self.final_states.add(state)


class NFA:
    def __init__(self, tree):
        self.tree = tree
        self.afn = AFN()
        self.state_counter = 0

    def convert(self):
        self.tree_to_afn(self.tree)
        return self.afn

    def tree_to_afn(self, node):
        if node is None:
            return

        if node.name == '*':
            self.tree_to_afn(node.leftLeaf)

            state_from = self.get_new_state()
            state_to = self.get_new_state()

            self.afn.add_transition(state_from, 'ε', node.leftLeaf.state_from)
            self.afn.add_transition(state_from, 'ε', state_to)
            self.afn.add_transition(
                node.leftLeaf.state_to, 'ε', node.leftLeaf.state_from)
            self.afn.add_transition(node.leftLeaf.state_to, 'ε', state_to)

            node.state_from = state_from
            node.state_to = state_to

        elif node.name == '.':

            temp = AFN()

            temp.start_state = [self.state_counter, 0]
            self.state_counter += 1
            temp.add_state(temp.start_state)

            self.tree_to_afn(node.leftLeaf)
            self.tree_to_afn(node.rightLeaf)

            self.afn.add_transition(
                node.leftLeaf.state_to, 'ε', node.rightLeaf.state_from)

            node.state_from = node.leftLeaf.state_from
            node.state_to = node.rightLeaf.state_to

        elif node.name == '|':
            self.tree_to_afn(node.leftLeaf)
            self.tree_to_afn(node.rightLeaf)

            state_from = self.get_new_state()
            state_to = self.get_new_state()

            self.afn.add_transition(state_from, 'ε', node.leftLeaf.state_from)
            self.afn.add_transition(state_from, 'ε', node.rightLeaf.state_from)
            self.afn.add_transition(node.leftLeaf.state_to, 'ε', state_to)
            self.afn.add_transition(node.rightLeaf.state_to, 'ε', state_to)

            node.state_from = state_from
            node.state_to = state_to

        elif node.name == '?':
            self.tree_to_afn(node.leftLeaf)

            state_from = self.get_new_state()
            state_to = self.get_new_state()

            self.afn.add_transition(state_from, 'ε', node.leftLeaf.state_from)
            self.afn.add_transition(state_from, 'ε', state_to)
            self.afn.add_transition(node.leftLeaf.state_to, 'ε', state_to)

            node.state_from = state_from
            node.state_to = state_to

        elif node.name == 'ε':
            state_from = self.get_new_state()
            state_to = self.get_new_state()
            self.afn.add_transition(state_from, 'ε', state_to)

            node.state_from = state_from
            node.state_to = state_to

        elif node.name == 'symbol':
            state_from = self.get_new_state()
            state_to = self.get_new_state()

            self.afn.add_transition(state_from, node.symbol, state_to)

            node.state_from = state_from
            node.state_to = state_to

    def get_new_state(self):
        state = 'q' + str(self.state_counter)
        self.state_counter += 1
        self.afn.add_state(state)
        return state
