from multiprocessing import Queue
from queue import PriorityQueue
from typing import Dict, Optional, List

from structures.Puzzle import Puzzle
from structures.PuzzleNode import PuzzleNode


def a_star_search(puzzle: Puzzle, heuristic, queue: Queue):
    start = PuzzleNode(puzzle)
    goal: PuzzleNode = PuzzleNode(puzzle)

    visited: List[Puzzle] = []
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from: Dict[PuzzleNode, Optional[PuzzleNode]] = {}
    cost_so_far: Dict[PuzzleNode, int] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: PuzzleNode = frontier.get()[1]
        visited.append(current.what_am_i)

        if current.what_am_i.is_solved():
            goal = current
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
                frontier.put((priority, nei))
                came_from[nei] = current

    goal_path: List[PuzzleNode] = []
    current = goal
    while not current.what_am_i.equals(start.what_am_i):
        if current not in came_from:
            goal_path = []
        goal_path.append(current)
        current = came_from[current]

    goal_path.append(start)
    goal_path.reverse()

    queue.put((goal_path, visited))


def many_slots_in_correct_place_heuristic(state: PuzzleNode) -> int:
    return state.what_am_i.how_many_incorrect_positions()


def atar_incorrect_position_heuristic(puzzle: Puzzle, queue: Queue):
    a_star_search(puzzle, many_slots_in_correct_place_heuristic, queue)


def distance_to_incorrect_heuristic(state: PuzzleNode) -> int:
    return state.what_am_i.how_far_from_correct_positions()


def atar_distance_to_incorrect(puzzle: Puzzle, queue: Queue):
    a_star_search(puzzle, distance_to_incorrect_heuristic, queue)
