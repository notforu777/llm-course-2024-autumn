import random

from fsm import FSM, build_odd_zeros_fsm


def get_valid_tokens(vocab: dict[int, str], eos_token_id: int, fsm: FSM, state: int) -> list[int]:
    valid_tokens = []
    
    transitions = fsm.states[state].transitions
    
    for token_id, token in vocab.items():
        if fsm.validate_continuation(state, token):
            valid_tokens.append(token_id)
        if token_id == eos_token_id and fsm.is_terminal(state):
            valid_tokens.append(eos_token_id)
        elif token in transitions:
            valid_tokens.append(token_id)
    
    return valid_tokens


def random_generation() -> str:
    # Define our vocabulary
    vocab = {0: "[EOS]", 1: "0", 2: "1"}
    eos_token_id = 0
    # Init Finite-State Machine
    fsm, state = build_odd_zeros_fsm()

    # List with generate tokens
    tokens: list[int] = []
    # Sample until EOS token
    while True:
        # 1. Get valid tokens
        valid_tokens = get_valid_tokens(vocab, eos_token_id, fsm, state)
        
        # 2. Get next token (randomly select from valid tokens)
        next_token = random.choice(valid_tokens)
        
        # 3. End generation or move to next iteration
        if next_token == eos_token_id:
            break
        
        tokens.append(next_token)
        state = fsm.states[state].transitions[vocab[next_token]]
        state = fsm.states.index(state)

    # Convert tokens to string
    return "".join([vocab[it] for it in tokens])


if __name__ == "__main__":
    print(random_generation())
