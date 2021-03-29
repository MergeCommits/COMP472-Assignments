import numpy
import math
import random
import time

heuristicFunction = None
algorithmFunction = None
nodeDic = {}
openDic = {}
openList = []
closedDic = {}
depthHop = 3

class Node:

    def __init__(self, state, parent, cost):
        self.stateID = None
        self.state = None
        self.parent = parent
        self.cost = cost
        self.children = None
        self.heuristic = 0

        self.setState(state)
        self.generateChildren()
        self.setHeuristic()

    def getState(self):
        return numpy.array(self.state)

    def setState(self, state):
        if isinstance(state, str):
            self.state = self.stringToState(state)
            self.stateID = state
        else:
            self.state = state
            self.stateID = self.stateToString(state)

    def generateChildren(self):
        self.children = []

        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                if i < self.state.shape[0]-1:
                    child = numpy.array(self.state)
                    child[i][j], child[i+1][j] = child[i+1][j], child[i][j]
                    self.children.append(self.stateToString(child))

                if j < self.state.shape[1]-1:
                    child = numpy.array(self.state)
                    child[i][j], child[i][j+1] = child[i][j+1], child[i][j]
                    self.children.append(self.stateToString(child))

    def __str__(self):
        grid = ""
        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                grid += str(self.state[i][j]) + " "
            grid += "\n"

        return grid

    def getChildren(self):
        return self.children[:]

    def setChildren(self, children):
        self.children = children

    def discoverChildren(self):
        childrenNodes = []

        for childID in self.children:
            if childID not in nodeDic:
                childNode = Node(childID, self, self.cost+1)
                nodeDic[id] = childNode
                childrenNodes.append(childNode)
            else:
                childNode = nodeDic[childID]
                childrenNodes.append(childNode)

        return childrenNodes

    def setHeuristic(self):
        self.heuristic = heuristicFunction(self.state)

    @staticmethod
    def stateToString(state):
        stateID = ""

        for i in range(state.shape[0]):
            for j in range(state.shape[1]):
                stateID += str(state[i][j]) + " "

        return stateID

    @staticmethod
    def stringToState(stateID):
        #print(stateID)
        stateList = stateID.split()
        state = numpy.zeros(len(stateList), dtype='int')
        for i in range(len(stateList)):
            state[i] = int(stateList[i])

        size = int(math.sqrt(len(stateList)))

        state = state.reshape([size, size])

        #print(state)
        return state


class Result():
    def __init__(self, searchPath, solutionPath, time, error=0):
        self.searchPath = searchPath
        self.solutionPath = solutionPath
        self.searchLength = len(searchPath)
        self.solutionLength = 0
        self.time = time
        self.error = error

        if solutionPath:
            self.solutionLength = len(solutionPath)

    def printToFile(self, fileName):
        textToWrite = "Start state:\n\n"
        textToWrite += str(self.searchPath[0])
        textToWrite += f"\nExplored nodes: {self.searchLength}\n"
        textToWrite += f"Time elapsed: {self.time}\n"

        if self.error == 0:
            textToWrite += f"Solution length: {self.solutionLength}\n\n"
            textToWrite += "============= Solution Path =============\n\n"

            for i in range(len(self.solutionPath)):
                if i > 0:
                    foundDifference = False
                    for x in range(self.solutionPath[i].state.shape[0]):
                        for y in range(self.solutionPath[i].state.shape[0]):
                            if self.solutionPath[i-1].state[x][y] != self.solutionPath[i].state[x][y]:
                                if x < self.solutionPath[i].state.shape[0]-1 and self.solutionPath[i-1].state[x+1][y] != self.solutionPath[i].state[x+1][y]:
                                    textToWrite += f"\nSwap {self.solutionPath[i].state[x][y]} with {self.solutionPath[i].state[x+1][y]}.\n\n"
                                else:
                                    textToWrite += f"\nSwap {self.solutionPath[i].state[x][y]} with {self.solutionPath[i].state[x][y+1]}.\n\n"

                                foundDifference = True
                                break

                        if foundDifference:
                            break

                textToWrite += str(self.solutionPath[i])

        elif self.error == 1:
            textToWrite += "No solution could be found. Reason: Was not able to reach the goal."
        elif self.error == 2:
            textToWrite += "No solution could be found. Reason: Ran out of time."

        file = open(fileName + ".txt", "w")
        file.write(textToWrite)
        file.close()

        textToWrite = ""
        for node in self.searchPath:
            textToWrite += str(node) + "\n"

        file = open(fileName + "-searchPath.txt", "w")
        file.write(textToWrite)
        file.close()

def nullHeuristic(state):
    return 0


def heuristic1(state):
    value = 0
    size = state.shape[0]
    for i in range(size):
        for j in range(size):
            if state[i][j] != j+size*i+1:
                value += 1

    return value


def heuristic2(state):
    value = 0
    size = state.shape[0]
    for i in range(size):
        for j in range(size):
            number = state[i][j] - 1
            y = number % size
            x = (number - y)/size
            value += abs(x-i) + abs(y-j)

    return value/2


def depthSelect(discoveredNodes):
    if len(openList) == 0:
        return None

    node = openList.pop()
    openDic.pop(node.stateID)
    return node


def iterativeSelect(discoveredNodes):
    if len(openList) == 0:
        return None

    lowestCost = openList[0].cost
    maxDepth = lowestCost - lowestCost%depthHop + depthHop

    for i in range(len(openList))[::-1]:
        if openList[i].cost <= maxDepth:
            node = openList.pop(i)
            openDic.pop(node.stateID)
            return node

    return None


def astarSelect(discoveredNodes):
    if len(openList) == 0:
        return None

    lowestCost = openList[0].cost + openList[0].heuristic
    lowestIndex = 0
    for i in range(1, len(openList)):
        cost = openList[i].cost + openList[i].heuristic
        if cost < lowestCost:
            lowestCost = cost
            lowestIndex = i

    node = openList.pop(lowestIndex)
    openDic.pop(node.stateID)
    #print(f"{node.cost} + {node.heuristic} = {lowestCost}")
    #print(node.state)
    return node



def main():
    print("What do you want to do?\n" +
          "1: Generate and analyse 20 puzzles\n" +
          "2: Analyse 20 pre-generated puzzles\n" +
          "3: Custom puzzle\n")

    answer = input()

    if answer == "1":
        generate()
        analysis()
    elif answer == "2":
        analysis()
    elif answer == "3":
        custom()
    else:
        print("Incorrect value. Please run the program again.")


def generate():
    textToWrite = ""
    size = 3

    for i in range(20):
        listState = list(range(1, size ** 2 + 1))
        random.shuffle(listState)
        numpyState = numpy.array(listState).reshape([size, size])
        stateID = Node.stateToString(numpyState)
        textToWrite += stateID + "\n"

    file = open("20puzzles.txt", "w")
    file.write(textToWrite)
    file.close()


def load():
    file = open("20puzzles.txt", "r")
    puzzleText = file.read()
    file.close()

    puzzleIDs = puzzleText.splitlines()
    puzzleStates = []

    for puzzleID in puzzleIDs:
        puzzleStates.append(Node.stringToState(puzzleID))

    return puzzleStates


def analysis():
    puzzles = load()
    size = 3

    results = [[], [], [], []]

    for i in range(20):
        numpyState = puzzles[i]
        print(f"Puzzle #{i+1}\n")
        print(numpyState)
        print("Processing using Depth-First...\n")
        results[0].append(algorithm(numpyState, True, "depth"))
        print("Processing using Iterative Deepening...\n")
        results[1].append(algorithm(numpyState, True, "iterative"))
        print("Processing using A* heuristic 1...\n")
        results[2].append(algorithm(numpyState, True, "astar", 1))
        print("Processing using A* heuristic 2...\n")
        results[3].append(algorithm(numpyState, True, "astar", 2))

    dfsText = resultAnalysis(results[0])
    iterText = resultAnalysis(results[1])
    astar1Text = resultAnalysis(results[2])
    astar2Text = resultAnalysis(results[3])

    optimalCounts = [0, 0, 0, 0]

    for i in range(20):
        lowestCost = 99999
        lowestIndex = -1
        lowestTime = 99999
        for j in range(len(results)):
            if results[j][i].error == 0:
                if results[j][i].solutionLength < lowestCost or (results[j][i].solutionLength == lowestCost and results[j][i].time < lowestTime):
                    lowestIndex = j
                    lowestCost = results[j][i].solutionLength
                    lowestTime = results[j][i].time

        if j >= 0:
            optimalCounts[j] += 1

    dfsText += f"Number of best results: {optimalCounts[0]}/20\n"
    iterText += f"Number of best results: {optimalCounts[1]}/20\n"
    astar1Text += f"Number of best results: {optimalCounts[2]}/20\n"
    astar2Text += f"Number of best results: {optimalCounts[3]}/20\n"

    finalText = "=========== Depth-First ============\n\n" + dfsText + "\n\n\n"
    finalText += "=========== Iterative-Deepening ============\n\n" + iterText + "\n\n\n"
    finalText += "=========== A* Heuristic #1 ============\n\n" + astar1Text + "\n\n\n"
    finalText += "=========== A* Heuristic #2 ============\n\n" + astar2Text + "\n\n\n"

    file = open("analysis.txt", "w")
    file.write(finalText)
    file.close()

    for i in range(20):
        results[0][i].printToFile(f"depthFirst/{i}")
        results[1][i].printToFile(f"iterative/{i}")
        results[2][i].printToFile(f"astar1/{i}")
        results[3][i].printToFile(f"astar2/{i}")

def resultAnalysis(results):
    count = 0
    success = 0
    totalSearchLength = 0
    totalSolutionLength = 0
    totalTime = 0

    for result in results:
        count += 1
        totalTime += result.time
        totalSearchLength += result.searchLength
        if result.error == 0:
            success += 1
            totalSolutionLength += result.solutionLength

    text = f"Success rate: {success}/{count}\n"
    text += f"Total execution time: {totalTime}\n"
    text += f"Average execution Time: {totalTime/count}\n"
    text += f"Total search length: {totalSearchLength}\n"
    text += f"Average search length: {totalSearchLength/count}\n"
    if success > 0:
        text += f"Total solution length: {totalSolutionLength}\n"
        text += f"Average solution length: {totalSolutionLength/count}"

    return text

def custom():
    print("What is the size of the puzzle?")
    size = int(input())

    print("Set a 60 second timer? (\"Yes\" or \"No\")")
    timered = input().lower() == "yes"

    print("Randomize the start state? (\"Yes\" or \"No\")")
    randomized = input().lower() == "yes"

    listState = list(range(1, size**2+1))

    if randomized:
        random.shuffle(listState)
    if not randomized:
        for i in range(len(listState)):
            print(f"Input the value in row {i%size}, column {(i - i%size)/size}.")
            listState[i] = int(input())

    numpyState = numpy.array(listState).reshape([size, size])

    print(numpyState)

    result = algorithm(numpyState, timered, "astar", 2)

    result.printToFile("customPuzzle")

    print("Analysis has been finished: customPuzzle.txt and customPuzzle-searchPath.txt have been created.")


def algorithm(startState, timered, algorithm, heuristic=None):
    global algorithmFunction
    global heuristicFunction

    if algorithm == "depth":
        algorithmFunction = depthSelect
    elif algorithm == "iterative":
        algorithmFunction = iterativeSelect
    elif algorithm == "astar":
        algorithmFunction = astarSelect

    if heuristic == None:
        heuristicFunction = nullHeuristic
    elif heuristic == 1:
        heuristicFunction = heuristic1
    elif heuristic == 2:
        heuristicFunction = heuristic2

    nodeDic.clear()
    openDic.clear()
    openList.clear()
    closedDic.clear()

    timelimit = 60
    if not timered:
        timelimit = 86400

    startTime = time.time()

    startNode = Node(startState, None, 0)
    currentNode = startNode

    size = startNode.state.shape[0]
    goalState = numpy.array(list(range(1, size**2+1))).reshape(size, size)
    goalStateID = Node.stateToString(goalState)

    searchPath = [currentNode]

    while currentNode.stateID != goalStateID and time.time() - startTime <= timelimit:
        discoveredNodes = currentNode.discoverChildren()
        exploredNodes = []
        for node in discoveredNodes:
            if node.parent.stateID != currentNode.stateID:
                if node.cost > currentNode.cost + 1:
                    node.parent = currentNode
                    node.cost = currentNode.cost + 1
                    exploredNodes.append(node)
                    if closedDic[node.stateID]:
                        closedDic.pop(node.stateID)
            else:
                exploredNodes.append(node)

        for node in exploredNodes:
            if node.stateID not in openDic:
                openDic[node.stateID] = node
                openList.append(node)

        currentNode = algorithmFunction(exploredNodes)
        if currentNode == None:
            break
        searchPath.append(currentNode)
        closedDic[currentNode.stateID] = currentNode

    totalTime = time.time() - startTime

    if currentNode.stateID != goalStateID:
        if totalTime > timelimit:
            return Result(searchPath, None, totalTime, error=2)
        else:
            return Result(searchPath, None, totalTime, error=1)

    solutionPath = [currentNode]
    while currentNode.stateID != startNode.stateID:
        currentNode = currentNode.parent
        solutionPath.append(currentNode)

    return Result(searchPath, solutionPath[::-1], totalTime)









main()