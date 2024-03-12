"""Automaton implementation."""

class State():
    """
    Definition of an automaton state. 

    Args:
        name: Name of the state.
        is_final: Whether the state is a final state or not.

    """

    def __init__(self, name, is_final = False):
        self.name = name
        self.is_final = is_final

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.name == other.name and self.is_final == other.is_final

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, is_final={self.is_final!r})"

    def __hash__(self):
        return hash(self.name)


class Transitions(dict):
    """
    Definition of all transitions in an automaton.
    Dictionary of initial states, where each state has a dictionary
    with the final states and the transition symbols. 


    Args:
        transitions: dictionary with a states as keys and dictionary of 
        symbol, final state as key, value tuple. 
        Example:
        {
            q1: {'a': {q2, q1}, None:{q3}}
            q2: {'a': {q3}, }
            q3: {None:{q1}, 'b':{q2}}
        }

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{[f'{key}:{self[key]}' for key in self.keys()]})"
        )
        
   

   
    def add_transition(self, start_state, symbol, end_state):
        """
            Checks that the transition or symbol is not in use and 
            adds one

            Args:
                state: initial state of the transition
                symbol: symbol of the transition
                end_state: final state of the transition
            Returns:
                None
        """

        if self.has_transition_to(start_state, symbol, end_state):
            raise ValueError("Repeated transition or symbol for state '%s'"%start_state)
        
        if self.has_transition(start_state, symbol):
            self[start_state][symbol].add(end_state)
        elif start_state in self.keys():
            self[start_state][symbol] = {end_state}
        else:
            self[start_state] = {symbol: {end_state}}

            
    def add_transitions(self, transitions):
        """
            Add transitions from a list

            Args:
                transitions: list of transitions (start, symbol, end)
            Returns:
                None
        """
        for (start_state, symbol, end_state) in transitions:
            self.add_transition(start_state, symbol, end_state)
    
    def has_transition(self, start_state, symbol):
        """
            Checks if a transition defined by a start_state and a symbol is
            contained in Transitions.
        """
        if start_state in self.keys() and symbol in self[start_state]:
            return True
        return False
    
    def has_transition_to(self, start_state, symbol, end_state):
        """
            Checks if a transition defined by a start_state, symbol and end_state
            is contained in Transitions.

            Args:
                state: initial state of the transition
                symbol: symbol of the transition
                end_state: final state of the transition
            Returns:
                True/False
        """
        if start_state in self and symbol in self[start_state]:
            return end_state in self[start_state][symbol]
        return False


    def get_transition(self, state, symbol):
        """
            Returns the corresponding set of states of a initial state and a symbol
            if Transitions has such transition. 

            Args:
                state: initial state of the transition
                symbol: symbol of the transition
            Returns:
                set of states
        """
        transitions = set()


        if not self.has_transition(state, symbol): 
            return transitions
        
        for q in self:
            if repr(q) == repr(state): 
                for symb in self[q]:
                    if symb is symbol: return self[q][symb]

        return transitions
    
    def get_all_transitions(self):
        """
            Returns all transitions in a list.

            Returns:
                list of triplets of transitions
        """

        all_transitions = []

        for start_state in self.keys():
            for symbol in self[start_state]:
                for end_state in self[start_state][symbol]:
                    all_transitions.append((start_state, symbol, end_state))
        
        return all_transitions
        
    

class FiniteAutomaton():
    """Automaton.
    Definiition of a Finite Automaton

    Args:
        initial_state: The initial state of the automaton.
        states: List of states (List[State]) of the automaton. It is converted to a
            tuple internally.
        symbols: List of symbols (List[str]) of the automaton. It is converted to a
            tuple internally.
        transitions: Transitions (Transition) from automaton.

    """

    def __init__(
        self,
        initial_state, states, symbols, transitions,
    ):

        if initial_state not in states:
            raise ValueError(
                f"Initial state {initial_state.name} "
                f"is not in the set of states",
            )

        """
        Check that there are no states with the same name.
        """
        if len(set(states)) != len(states):
            raise ValueError("There are repeated states")

        """
        Check that there are no repeated symbols.
        """
        if len(set(symbols)) != len(symbols):
            raise ValueError("There are repeated symbols")

        self.initial_state = initial_state
        self.states = states
        self.symbols = symbols
        self.transitions = Transitions(transitions)
        

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        # We use sets as the order should not matter
        return (
            self.initial_state == other.initial_state
            and set(self.states) == set(other.states)
            and set(self.symbols) == set(other.symbols)
            and set(self.transitions) == set(other.transitions)
        )

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"initial_state={self.initial_state!r}, "
            f"states={self.states!r}, "
            f"symbols={self.symbols!r}, "
            f"transitions={self.transitions!r})"
        )

    def add_transition(self, start_state, symbol, end_state):
        self.transitions.add_transition(start_state, symbol, end_state)
        
    def add_transitions(self, transitions):
        self.transitions.add_transitions(transitions)

    def has_transition(self, state, symbol):
        return self.transitions.has_transition(state, symbol)
        
    def get_transition(self, state, symbol):
        return self.transitions.get_transition(state, symbol)
        
    def get_all_transitions(self):
        return self.transitions.get_all_transitions()
        
    def to_deterministic(self):
        from automata.dfa import DeterministicFiniteAutomaton
        return DeterministicFiniteAutomaton.to_deterministic(self)