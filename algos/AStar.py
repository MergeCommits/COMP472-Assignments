from typing import Dict, Optional

from structures.PriorityQueue import PriorityQueue
from structures.Puzzle import Puzzle
from structures.PuzzleNode import PuzzleNode


def a_star_search(puzzle: Puzzle, heuristic):
    start = PuzzleNode(puzzle)

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict[PuzzleNode, Optional[PuzzleNode]] = {}
    cost_so_far: Dict[PuzzleNode, int] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: PuzzleNode = frontier.get()

        if current.what_am_i.is_solved():
            break

        permutes = current.what_am_i.get_permutations()

        for permutation in permutes:
            new_node = PuzzleNode(permutation)
            new_node.parent = current
            current.children.append(new_node)

        for nei in current.children:
            new_cost = cost_so_far[current] + 1
            if nei not in cost_so_far or new_cost < cost_so_far[nei]:
                cost_so_far[nei] = new_cost
                priority = new_cost + heuristic(nei)
                frontier.put(nei, priority)
                came_from[nei] = current

    return came_from, cost_so_far
