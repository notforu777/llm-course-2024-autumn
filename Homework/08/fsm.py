from dataclasses import dataclass, field
from typing import Optional


@dataclass
class State:
    is_terminal: bool
    transitions: dict[str, "State"] = field(default_factory=dict)

    def add_transition(self, char, state):
        self.transitions[char] = state


class FSM:
    def __init__(self, states: list[State], initial: int):
        self.states = states
        self.initial = initial

    def is_terminal(self, state_id):
        return self.states[state_id].is_terminal

    def move(self, line: str, start: Optional[int] = None) -> Optional[int]:
        if start is None:
            start = self.initial
        
        current_state = self.states[start]
        
        for char in line:
            if char in current_state.transitions:
                current_state = current_state.transitions[char]
            else:
                return None
        
        return self.states.index(current_state)

    def accept(self, candidate: str) -> bool:
        end_state = self.move(candidate)
        return end_state is not None and self.is_terminal(end_state)

    def validate_continuation(self, state_id: int, continuation: str) -> bool:
        current_state = self.states[state_id]
        
        for char in continuation:
            if char in current_state.transitions:
                current_state = current_state.transitions[char]
            else:
                return False
        
        return True



def build_odd_zeros_fsm() -> tuple[FSM, int]:
    state_even = State(is_terminal=False)
    state_odd = State(is_terminal=True)
    
    state_even.add_transition('0', state_odd)
    state_even.add_transition('1', state_even)
    
    state_odd.add_transition('0', state_even)
    state_odd.add_transition('1', state_odd)
    
    fsm = FSM(states=[state_even, state_odd], initial=0)
    
    return fsm, 0



if __name__ == "__main__":
    _fsm, _ = build_odd_zeros_fsm()
    print("101010 -- ", _fsm.accept("101010"))
    print("10101 -- ", _fsm.accept("10101"))
