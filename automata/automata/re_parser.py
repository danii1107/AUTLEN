"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton, State, Transitions

def _re_to_rpn(re_string):
    """
    Convert re to reverse polish notation (RPN).

    Does not check that the input re is syntactically correct.

    Args:
        re_string: Regular expression in infix notation. Type: str

    Returns:
        Regular expression in reverse polish notation. Type: str

    """
    stack = [] # List of strings
    rpn_string = ""
    for x in re_string:
        if x == "+":
            while len(stack) > 0 and stack[-1] != "(":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == ".":
            while len(stack) > 0 and stack[-1] == ".":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == "(":
            stack.append(x)
        elif x == ")":
            while stack[-1] != "(":
                rpn_string += stack.pop()
            stack.pop()
        else:
            rpn_string += x

    while len(stack) > 0:
        rpn_string += stack.pop()

    return rpn_string



class REParser():
    """Class for processing regular expressions in Kleene's syntax."""

    def __init__(self) -> None:
        self.state_counter = 0

    def _create_automaton_empty(self):
        """
        Create an automaton that accepts the empty language.

        Returns:
            Automaton that accepts the empty language. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        states = []

        q = State(str(self.state_counter), is_final=False)
        states.append(q)
        self.state_counter += 1

        qf = State(str(self.state_counter), is_final=True)
        states.append(qf)
        self.state_counter += 1

        return FiniteAutomaton(initial_state=q, 
                                states=states,
                                symbols=(), 
                                transitions=())
        #---------------------------------------------------------------------


    def _create_automaton_lambda(self):
        """
        Create an automaton that accepts the empty string.

        Returns:
            Automaton that accepts the empty string. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        states = []

        q = State(str(self.state_counter), is_final=False)
        states.append(q)
        self.state_counter += 1

        qf = State(str(self.state_counter), is_final=True)
        states.append(qf)
        self.state_counter += 1

        transitions = Transitions()
        transitions.add_transition(q, None, qf)

        return FiniteAutomaton(initial_state=q, 
                                states=states,
                                symbols=(), 
                                transitions=transitions)
        #---------------------------------------------------------------------


    def _create_automaton_symbol(self, symbol):
        """
        Create an automaton that accepts one symbol.

        Args:
            symbol: Symbol that the automaton should accept. Type: str

        Returns:
            Automaton that accepts a symbol. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        states = []

        q = State(str(self.state_counter), is_final=False)
        states.append(q)
        self.state_counter += 1

        qf = State(str(self.state_counter), is_final=True)
        states.append(qf)
        self.state_counter += 1

        transitions = Transitions()
        transitions.add_transition(q, symbol, qf)

        return FiniteAutomaton(initial_state=q, 
                                states=states,
                                symbols=symbol, 
                                transitions=transitions)
        #---------------------------------------------------------------------


    def _create_automaton_star(self, automaton):
        """
        Create an automaton that accepts the Kleene star of another.

        Args:
            automaton: Automaton whose Kleene star must be computed. Type: FiniteAutomaton

        Returns:
            Automaton that accepts the Kleene star. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        states = []
        
        q = State(str(self.state_counter), is_final=False)
        self.state_counter += 1
        qf = State(str(self.state_counter), is_final=True)
        self.state_counter += 1

        states.append(q)
        states.append(qf)
        
        transitions = Transitions()
        transitions.add_transition(q, None, qf)
        transitions.add_transition(q, None, automaton.initial_state)
        
        for state in automaton.states:
            if state.is_final is True:
                transitions.add_transition(state, None, automaton.initial_state) 
                transitions.add_transition(state, None, qf) 
                state.is_final = False      
            states.append(state)
        
        all_transitions = automaton.transitions.get_all_transitions()
        for transition in all_transitions:
            transitions.add_transition(transition[0], 
                                       transition[1], 
                                       transition[2])
        
        return FiniteAutomaton(initial_state=q, 
                                states=states,
                                symbols=automaton.symbols, 
                                transitions=transitions)
        #---------------------------------------------------------------------


    def _create_automaton_union(self, automaton1, automaton2):
        """
        Create an automaton that accepts the union of two automata.

        Args:
            automaton1: First automaton of the union. Type: FiniteAutomaton.
            automaton2: Second automaton of the union. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the union. Type: FiniteAutomaton.

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        states = []
        
        q = State(str(self.state_counter), is_final=False)
        self.state_counter += 1
        qf = State(str(self.state_counter), is_final=True)
        self.state_counter += 1

        states.append(q)
        states.append(qf)

        transitions = Transitions()
        transitions.add_transition(q, None, automaton1.initial_state)
        transitions.add_transition(q, None, automaton2.initial_state)
        
        for state in automaton1.states:
            if state.is_final is True:
                transitions.add_transition(state, None, qf)
                state.is_final = False
            states.append(state)

        for state in automaton2.states:
            if state.is_final is True:
                transitions.add_transition(state, None, qf)
                state.is_final = False
            states.append(state)

        all_transitions_1 = automaton1.transitions.get_all_transitions()
        for transition in all_transitions_1:
            transitions.add_transition(transition[0], 
                                       transition[1], 
                                       transition[2])

        all_transitions_2 = automaton2.transitions.get_all_transitions() 
        for transition in all_transitions_2:
            transitions.add_transition(transition[0], 
                                       transition[1], 
                                       transition[2])

        symbols = set(automaton1.symbols).intersection(automaton2.symbols)

        return FiniteAutomaton(initial_state=q, 
                                states=states,
                                symbols=symbols, 
                                transitions=transitions)
        #---------------------------------------------------------------------


    def _create_automaton_concat(self, automaton1, automaton2):
        """
        Create an automaton that accepts the concatenation of two automata.

        Args:
            automaton1: First automaton of the concatenation. Type: FiniteAutomaton.
            automaton2: Second automaton of the concatenation. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the concatenation. Type: FiniteAutomaton.

        """
        #---------------------------------------------------------------------
        # TO DO: Implement this method...
        states = automaton1.states + automaton2.states

        for state in states:
            state = str(self.state_counter)
            self.state_counter += 1

        transitions = Transitions()

        q = automaton1.initial_state

        for state in automaton1.states:
            if state.is_final is True:
                transitions.add_transition(state, None, automaton2.initial_state)
                state.is_final = False

        all_transitions_1 = automaton1.transitions.get_all_transitions()
        for transition in all_transitions_1:
            transitions.add_transition(transition[0], 
                                       transition[1], 
                                       transition[2])

        all_transitions_2 = automaton2.transitions.get_all_transitions()
        for transition in all_transitions_2:
            transitions.add_transition(transition[0], 
                                       transition[1], 
                                       transition[2])

        symbols = set(automaton1.symbols).union(automaton2.symbols)

        return FiniteAutomaton(initial_state=q, 
                                states=states,
                                symbols=symbols, 
                                transitions=transitions)
        #---------------------------------------------------------------------


    def create_automaton(
        self,
        re_string,
    ):
        """
        Create an automaton from a regex.

        Args:
            re_string: String with the regular expression in Kleene notation. Type: str

        Returns:
            Automaton equivalent to the regex. Type: FiniteAutomaton

        """
        if not re_string:
            return self._create_automaton_empty()

        rpn_string = _re_to_rpn(re_string)

        stack = [] # list of FiniteAutomatons

        self.state_counter = 0
        for x in rpn_string:
            if x == "*":
                aut = stack.pop()
                stack.append(self._create_automaton_star(aut))
            elif x == "+":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_union(aut1, aut2))
            elif x == ".":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_concat(aut1, aut2))
            elif x == "λ":
                stack.append(self._create_automaton_lambda())
            else:
                stack.append(self._create_automaton_symbol(x))

        return stack.pop()