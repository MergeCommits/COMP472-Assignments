import sympy
import math


class State:
    nodesVisited = 0
    nodesEvaluated = 0
    maxDepth = 0
    subtreeCount = 0
    branchCount = 0

    def __init__(self, availableTokens, lastToken, currentPlayer, depth=-1):
        self.availableTokens = availableTokens
        self.lastToken = lastToken
        self.actions = None
        self.currentPlayer = currentPlayer
        self.depth = depth

        self.generateActions()

        State.nodesVisited += 1

    def generateActions(self):
        if self.availableTokens is None:
            return

        self.actions = []
        for token in self.availableTokens:
            if max(token, self.lastToken) % min(token, self.lastToken) == 0:
                self.actions.append(token)

    def __str__(self):
        return f"Player {self.currentPlayer}'s turn: [{self.lastToken}] => {self.availableTokens}"

    def heuristic(self):
        heuristic = float(0)

        # Case: Dead end. Defeat.
        if len(self.actions) == 0:
            heuristic = -1

        # Case: 1 is still available to take.
        elif 1 in self.actions:
            heuristic = 0

        # Case: 2 is the last picked token.
        elif self.lastToken == 1:
            if len(self.availableTokens) % 2 == 1:
                heuristic = 0.5
            else:
                heuristic = -0.5

        # Case: 3 is not available, and last picked token is a prime.
        elif sympy.isprime(self.lastToken):
            if len(self.actions) % 2 == 1:
                heuristic = 0.7
            else:
                heuristic = -0.7

        # Case: 4 is not available, and last picked token is a composite.
        else:
            largestPrime = 0
            for token in self.actions:
                if self.lastToken % token == 0 and sympy.isprime(token) and token > largestPrime:
                    largestPrime = token

            if largestPrime == 0:
                if len(self.actions) % 2 == 1:
                    heuristic = 0.7
                else:
                    heuristic = -0.7

            else:
                multiples = 0
                for token in self.availableTokens:
                    if token % largestPrime == 0:
                        multiples += 1

                if multiples % 2 == 1:
                    heuristic = 0.6
                else:
                    heuristic = -0.6

        # Flip if it's Min's turn.
        if self.currentPlayer == "Min":
            heuristic *= -1

        State.nodesEvaluated += 1

        return heuristic

    def analyzeInput(self, inputState):
        parameters = inputState.split()

        tokenCount = int(parameters[0])
        self.availableTokens = list(range(1, tokenCount + 1))

        turnNum = int(parameters[1])
        if turnNum % 2 == 0:
            self.currentPlayer = "Max"
        else:
            self.currentPlayer = "Min"

        # If the input is not a fresh game.
        if turnNum > 0:
            for i in parameters[2:2 + turnNum]:
                self.availableTokens.remove(int(i))

            self.lastToken = int(parameters[-2])

            self.generateActions()

        # If the input is a fresh game.
        else:
            self.actions = []
            for i in range(1, math.ceil(tokenCount / 2), 2):
                self.actions.append(i)

        self.depth = int(parameters[-1])
        if self.depth == 0:
            self.depth = -1

    def generateChild(self, action):
        newTokens = self.availableTokens.copy()
        newTokens.remove(action)

        return State(newTokens, action, self.getOppositePlayer(), self.depth - 1)

    def getOppositePlayer(self):
        if self.currentPlayer == "Min":
            return "Max"
        else:
            return "Min"

    @staticmethod
    def updateBranchingFactor(count):
        State.subtreeCount += 1
        State.branchCount += count


def main():
    print(
        "Input the state of the game: <amount of tokens> <turns elapsed> <tokens taken in order> <max depth evaluation>")
    stateInput = input()

    startNode = State(None, 0, "")
    startNode.analyzeInput(stateInput)
    result = alphaBetaPruning(startNode, -math.inf, math.inf)

    print(f"Move: {result[1]}")
    print(f"Value: {result[0]}")
    print(f"Number of Nodes Visited: {State.nodesVisited}")
    print(f"Number of Nodes Evaluated: {State.nodesEvaluated}")
    print(f"Max Depth Reached: {State.maxDepth}")
    print(f"Avg Effective Branching Factor: {State.branchCount / State.subtreeCount}")


def alphaBetaPruning(state, alpha, beta, depth=0):
    if (State.maxDepth < depth):
        State.maxDepth = depth

    print(f"{'    ' * depth}{state}")
    if len(state.actions) == 0 or state.depth == 0:
        return [state.heuristic(), None]

    bestScore = None
    bestAction = None
    totalActionsExamined = 0

    for action in state.actions:
        totalActionsExamined += 1
        changed = False
        childState = state.generateChild(action)
        score = alphaBetaPruning(childState, alpha, beta, depth + 1)[0]
        print(f"{'    ' * (depth + 1)}{score}")
        if bestScore is None:
            bestScore = score
            bestAction = action
            changed = True

        else:
            if state.currentPlayer == "Max":
                if score > bestScore:
                    bestScore = score
                    bestAction = action
                    changed = True
            else:
                if score < bestScore:
                    bestScore = score
                    bestAction = action
                    changed = True

        if changed:
            if state.currentPlayer == "Max":
                if bestScore > alpha:
                    alpha = bestScore
            else:
                if bestScore < beta:
                    beta = bestScore

            if alpha >= beta:
                State.updateBranchingFactor(totalActionsExamined)
                return [bestScore, bestAction]

    State.updateBranchingFactor(totalActionsExamined)
    return [bestScore, bestAction]


main()
