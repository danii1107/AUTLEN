from automata.automaton import State, Transitions, FiniteAutomaton
from automata.utils import is_deterministic
from collections import deque
from functools import cmp_to_key
from typing import List
import numpy
import copy
import queue

def compare_states(state1, state2):
    name1 = state1.name.lower()
    name2 = state2.name.lower()

    if is_initial_state(name1):
        return -1
    elif is_initial_state(name2):
        return 1
    if is_empty_state(name1):
        return 1
    elif is_empty_state(name2):
        return -1
    if is_final_state(name1):
        return 1
    elif is_final_state(name2):
        return -1

    if are_digits_valid(name1) and are_digits_valid(name2):
        return compare_digits(name1, name2)

    val1 = calculate_value(name1)
    val2 = calculate_value(name2)

    return val1 - val2

def is_initial_state(name):
    return name == "initial"

def is_empty_state(name):
    return name == "empty"

def is_final_state(name):
    return name == "qf" or name == "final"

def are_digits_valid(name):
    return name[1:].isdigit()

def compare_digits(name1, name2):
    return int(name1[1:]) - int(name2[1:])

def calculate_value(name):
    return sum(ord(char) for char in name)


def combined_states(state_set: set) -> State:
    state_list = list(state_set)
    sorted_list = sort_states(state_list)

    new_state_name = ""
    is_final_state = False

    has_numbers = check_for_numbers(sorted_list)

    for state in sorted_list:
        new_state_name = construct_new_state_name(state, has_numbers, new_state_name)
        is_final_state = update_final_state_flag(state, is_final_state)

    return State(new_state_name, is_final_state)

def sort_states(states):
    return sorted(states, key=cmp_to_key(compare_states))

def check_for_numbers(states):
    if states[0].name[1:].isdigit():
        return True
    else:
        return False

def construct_new_state_name(state, has_numbers, current_name):
    if has_numbers:
        return current_name + "q" + state.name[1:]
    else:
        return current_name + state.name

def update_final_state_flag(state, current_flag):
    if state.is_final:
        return True
    else:
        return current_flag

from typing import List

def has_transitions_other_than_self(state: State, automaton: FiniteAutomaton) -> bool:
    for symbol in automaton.symbols:
        transitions = automaton.get_transition(state, symbol)
        if len(transitions) > 0 and any(q != state for q in transitions):
            return True
    return False

def find_empty_state(automaton: FiniteAutomaton) -> State:
    for state in automaton.states:
        if not has_transitions_other_than_self(state, automaton) and not state.is_final:
            return state

    return State("Empty", is_final=False)

def get_empty_state(automaton: FiniteAutomaton) -> State:
    return find_empty_state(automaton)


class DeterministicFiniteAutomaton(FiniteAutomaton):

    @staticmethod
    def to_deterministic(finiteAutomaton: FiniteAutomaton):
        """
        Returns an equivalent deterministic finite automaton.
        """

        # To avoid circular imports
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(finiteAutomaton)

        initial = combined_states(evaluator.current_states)
        table = dict()

        q = queue.Queue()
        q.put(evaluator.current_states)
        newstates = set()
        newstates.add(initial)

        empty_state = get_empty_state(finiteAutomaton)
        empty_flag = False

        while not q.empty():
            state = q.get()

            newstate = combined_states(state)

            for sym in finiteAutomaton.symbols:
                evaluator.current_states = state
                evaluator.process_symbol(sym)

                if newstate not in table.keys():
                    table[newstate] = dict()

                if len(evaluator.current_states) == 0:
                    process_state = empty_state
                    newstates.add(process_state)
                    empty_flag = True
                else:
                    process_state = combined_states(evaluator.current_states)

                table[newstate][sym] = set()
                table[newstate][sym].add(process_state)

                if process_state not in newstates:
                    newstates.add(process_state)
                    q.put(evaluator.current_states)
        
        if empty_flag:
            table[empty_state] = dict()
            for sym in finiteAutomaton.symbols:
                table[empty_state][sym] = set()
                table[empty_state][sym].add(empty_state)

        trans = Transitions(table)

        return FiniteAutomaton(initial,
                                states=newstates,
                              symbols=finiteAutomaton.symbols, 
                              transitions=trans)

    @staticmethod
    def to_minimized(dfa):
        """
        Return a equivalent minimal automaton.
        Returns:
            Equivalent minimal automaton.
        """

        # To avoid circular imports
        from automata.automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(dfa)
        evaluatorpre = FiniteAutomatonEvaluator(dfa)

        q = queue.Queue()
        q.put(evaluator.current_states)

        # set of accesible states
        accesible_states = set()
        accesible_states.add(dfa.initial_state)

        # while is not empty
        while not q.empty():
            # it will extract the next state on queue
            state = q.get()

            # loop to check all the transitions of that state
            for sym in dfa.symbols:

                # current states is now the extracted state
                evaluator.current_states = state

                # evaluate it
                evaluator.process_symbol(sym)

                # if there are states on current_states
                if len(evaluator.current_states) > 0:
                    # flag to check if the current states have been added to queue
                    flag_addqueue = False

                    for next_state in evaluator.current_states:
                        # if the next state has not been added
                        if next_state not in accesible_states:

                            if not flag_addqueue:
                                # add current states if flag is false
                                q.put(evaluator.current_states)
                                flag_addqueue = True

                            # add the next state to accesible states
                            accesible_states.add(next_state)

        # sorted list of the states
        accesible_list = sorted(list(accesible_states),
                                key=cmp_to_key(compare_states))

        # create an array for the equivalence
        xtable = len(accesible_list)
        class_table = numpy.ndarray(shape=(2, xtable))

        # first iteration
        for i in range(xtable):
            class_table[0][i] = int(accesible_list[i].is_final)
            class_table[1][i] = None

        while 1:
            # class counter
            classcont = 0
            for j in range(xtable):
                # if its NaN (None, without class)
                if numpy.isnan(class_table[1][j]):
                    # it gets one
                    class_table[1][j] = classcont
                    classcont += 1

                    # this is the loop that compares transitions
                    for i in range(1, xtable):
                        same_class = True

                        # if no class
                        if numpy.isnan(class_table[1][i]):
                            # and the next state on the previous row
                            # equals the previous class from the same state
                            # that we assigned the class on the top loop
                            if class_table[0][i] == class_table[0][j]:

                                # for each symbol
                                for sym in dfa.symbols:
                                    # checks transitions
                                    evaluatorpre.current_states = {
                                        accesible_list[j]}
                                    evaluator.current_states = {
                                        accesible_list[i]}
                                    evaluatorpre.process_symbol(sym)
                                    evaluator.process_symbol(sym)

                                    # gets the state itself
                                    pre_state = evaluatorpre.current_states.pop()
                                    state_now = evaluator.current_states.pop()

                                    # and checks if the classes dont match
                                    if class_table[0][accesible_list.index(pre_state)] != class_table[0][accesible_list.index(state_now)]:
                                        same_class = False
                                        break
                                # if al their transitions classes match, then assigns the value
                                # from the new assigned class on the top loop
                                if same_class:
                                    class_table[1][i] = class_table[1][j]

            # if both rows are equal its finished
            if numpy.array_equal(class_table[0], class_table[1]):
                break
            else:
                # if not the second row becomes the first
                for i in range(xtable):
                    class_table[0][i] = class_table[1][i]
                    class_table[1][i] = None

        # Checks the bigger class
        check_bigger = [class_table[0][i] for i in range(len(class_table[0]))]
        check_bigger.sort(reverse=True)
        new_tam_states = int(check_bigger[0])+1

        # list of sets for the new states
        list_set_states = [set() for i in range(new_tam_states)]
        new_states = set()

        for i in range(xtable):
            list_set_states[int(class_table[0][i])].add(accesible_list[i])

        new_transitions_dict = dict()

        for i in range(new_tam_states):
            # it creates the new states
            aux_state = combined_states(list_set_states[i])
            new_states.add(aux_state)

            new_transitions_dict[aux_state] = dict()

            for symbol in dfa.symbols:
                # and checks all transitions
                evaluator.current_states = list_set_states[i]
                evaluator.process_symbol(symbol)
                new_transitions_dict[aux_state][symbol] = set()

                # if its not on the list of set states
                if evaluator.current_states not in list_set_states:
                    aux_current = evaluator.current_states.pop()

                    # gets the index of the class (which is the same index for the set of the new state)
                    evaluator.current_states = list_set_states[int(class_table[0][accesible_list.index(
                        aux_current)])]
                
                # add the new state (creating it)
                new_transitions_dict[aux_state][symbol].add(
                    combined_states(evaluator.current_states))


        trans = Transitions(new_transitions_dict)

        aut = FiniteAutomaton(initial_state=combined_states(list_set_states[0]), states=new_states,
                              symbols=dfa.symbols, transitions=trans)

        return aut