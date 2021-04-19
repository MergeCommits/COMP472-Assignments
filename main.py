import sympy
import math


class State:
    nodes_visited = 0
    nodes_evaluated = 0
    max_depth = 0
    subtree_count = 0
    branch_count = 0

    def __init__(self, available_tokens, last_token, current_player, depth=-1):
        self.available_tokens = available_tokens
        self.last_token = last_token
        self.actions = None
        self.current_player = current_player
        self.depth = depth

        self.generate_actions()

        State.nodes_visited += 1

    def generate_actions(self):
        if self.available_tokens is None:
            return

        self.actions = []
        for token in self.available_tokens:
            if max(token, self.last_token) % min(token, self.last_token) == 0:
                self.actions.append(token)

    def __str__(self):
        return f"Player {self.current_player}'s turn: [{self.last_token}] => {self.available_tokens}"

    def heuristic(self):
        heuristic = float(0)

        # Case: Dead end. Defeat.
        if len(self.actions) == 0:
            heuristic = -1

        # Case: 1 is still available to take.
        elif 1 in self.actions:
            heuristic = 0

        # Case: 2 is the last picked token.
        elif self.last_token == 1:
            if len(self.available_tokens) % 2 == 1:
                heuristic = 0.5
            else:
                heuristic = -0.5

        # Case: 3 is not available, and last picked token is a prime.
        elif sympy.isprime(self.last_token):
            if len(self.actions) % 2 == 1:
                heuristic = 0.7
            else:
                heuristic = -0.7

        # Case: 4 is not available, and last picked token is a composite.
        else:
            largest_prime = 0
            for token in self.actions:
                if self.last_token % token == 0 and sympy.isprime(token) and token > largest_prime:
                    largest_prime = token

            if largest_prime == 0:
                if len(self.actions) % 2 == 1:
                    heuristic = 0.7
                else:
                    heuristic = -0.7

            else:
                multiples = 0
                for token in self.available_tokens:
                    if token % largest_prime == 0:
                        multiples += 1

                if multiples % 2 == 1:
                    heuristic = 0.6
                else:
                    heuristic = -0.6

        # Flip if it's Min's turn.
        if self.current_player == "Min":
            heuristic *= -1

        State.nodes_evaluated += 1

        return heuristic

    def analyze_input(self, input_state):
        parameters = input_state.split()

        token_count = int(parameters[0])
        self.available_tokens = list(range(1, token_count + 1))

        turn_num = int(parameters[1])
        if turn_num % 2 == 0:
            self.current_player = "Max"
        else:
            self.current_player = "Min"

        # If the input is not a fresh game.
        if turn_num > 0:
            for i in parameters[2:2 + turn_num]:
                self.available_tokens.remove(int(i))

            self.last_token = int(parameters[-2])

            self.generate_actions()

        # If the input is a fresh game.
        else:
            self.actions = []
            for i in range(1, math.ceil(token_count / 2), 2):
                self.actions.append(i)

        self.depth = int(parameters[-1])
        if self.depth == 0:
            self.depth = -1

    def generate_child(self, action):
        new_tokens = self.available_tokens.copy()
        new_tokens.remove(action)

        return State(new_tokens, action, self.get_opposite_player(), self.depth - 1)

    def get_opposite_player(self):
        if self.current_player == "Min":
            return "Max"
        else:
            return "Min"

    @staticmethod
    def update_branching_factor(count):
        State.subtree_count += 1
        State.branch_count += count


def main():
    print(
        "Input the state of the game: <amount of tokens> <turns elapsed> <tokens taken in order> <max depth evaluation>"
    )
    state_input = input()

    start_node = State(None, 0, "")
    start_node.analyze_input(state_input)
    result = alpha_beta_pruning(start_node, -math.inf, math.inf)

    print(f"Move: {result[1]}")
    value = "{:.1f}".format(result[0])
    print(f"Value: {value}")
    print(f"Number of Nodes Visited: {State.nodes_visited}")
    print(f"Number of Nodes Evaluated: {State.nodes_evaluated}")
    print(f"Max Depth Reached: {State.max_depth}")
    avg_branch_factor = "{:.1f}".format(State.branch_count / State.subtree_count)
    print(f"Avg Effective Branching Factor: {avg_branch_factor}")


def alpha_beta_pruning(state, alpha, beta, depth=0):
    if State.max_depth < depth:
        State.max_depth = depth

    print(f"{'    ' * depth}{state}")
    if len(state.actions) == 0 or state.depth == 0:
        return [state.heuristic(), None]

    best_score = None
    best_action = None
    total_actions_examined = 0

    for action in state.actions:
        total_actions_examined += 1
        changed = False
        child_state = state.generate_child(action)
        score = alpha_beta_pruning(child_state, alpha, beta, depth + 1)[0]
        print(f"{'    ' * (depth + 1)}{score}")
        if best_score is None:
            best_score = score
            best_action = action
            changed = True

        else:
            if state.current_player == "Max":
                if score > best_score:
                    best_score = score
                    best_action = action
                    changed = True
            else:
                if score < best_score:
                    best_score = score
                    best_action = action
                    changed = True

        if changed:
            if state.current_player == "Max":
                if best_score > alpha:
                    alpha = best_score
            else:
                if best_score < beta:
                    beta = best_score

            if alpha >= beta:
                State.update_branching_factor(total_actions_examined)
                return [best_score, best_action]

    State.update_branching_factor(total_actions_examined)
    return [best_score, best_action]


main()
