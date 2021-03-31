import sys
import time
from queue import PriorityQueue
from typing import Dict, Optional, List, Tuple

from analysis.Analysis import MAX_TIMEOUT
from structures.Puzzle import Puzzle
from structures.PuzzleNode import PuzzleNode


def was_visited(node: Puzzle, visited: List[Puzzle]) -> bool:
    for visit in visited:
        if node.equals(visit):
            return True

    return False


def inside_cost_so_far(node: PuzzleNode, cost_so_far: Dict[PuzzleNode, int]) -> bool:
    keys = cost_so_far.keys()
    for key in keys:
        if key.what_am_i.equals(node.what_am_i):
            return True

    return False


def has_cost_and_is_less_than(node: PuzzleNode, cost: int, cost_so_far: Dict[PuzzleNode, int]) -> int:
    keys = cost_so_far.keys()
    for key in keys:
        if key.what_am_i.equals(node.what_am_i):
            return cost < cost_so_far[key]

    print("Unexpected error:", sys.exc_info()[0])


def add_to_cost_so_far(node: PuzzleNode, cost: int, cost_so_far: Dict[PuzzleNode, int]) -> int:
    keys = cost_so_far.keys()
    for key in keys:
        if key.what_am_i.equals(node.what_am_i):
            cost_so_far.pop(key, None)
            break

    cost_so_far[node] = cost


def update_came_from(node: PuzzleNode, fro: PuzzleNode, came_from: Dict[PuzzleNode, Optional[PuzzleNode]]) -> int:
    keys = came_from.keys()
    for key in keys:
        if key.what_am_i.equals(node.what_am_i):
            came_from.pop(key, None)
            break

    came_from[node] = fro


def get_from_cost_so_far(node: PuzzleNode, cost_so_far: Dict[PuzzleNode, int]) -> int:
    keys = cost_so_far.keys()
    for key in keys:
        if key.what_am_i.equals(node.what_am_i):
            return cost_so_far[key]

    print("Unexpected error:", sys.exc_info()[0])


def a_star_search(puzzle: Puzzle, heuristic) -> Optional[Tuple[List[PuzzleNode], List[Puzzle], float]]:
    start = PuzzleNode(puzzle)
    goal: PuzzleNode = PuzzleNode(puzzle)

    visited: List[Puzzle] = []
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from: Dict[PuzzleNode, Optional[PuzzleNode]] = {}
    cost_so_far: Dict[PuzzleNode, int] = {}
    came_from[start] = start
    cost_so_far[start] = 0

    timeout = time.time() + MAX_TIMEOUT

    while not frontier.empty():
        if time.time() > timeout:
            return None

        current: PuzzleNode = frontier.get()[1]

        if not was_visited(current.what_am_i, visited):
            visited.append(current.what_am_i)
            # print("ALREADY")

        if current.what_am_i.is_solved():
            goal = current
            break

        permutes = current.what_am_i.get_permutations()

        for permutation in permutes:
            new_node = PuzzleNode(permutation)
            new_node.parent = current
            current.children.append(new_node)

        for nei in current.children:
            # new_cost = cost_so_far[current] + 1
            new_cost = get_from_cost_so_far(current, cost_so_far) + 1
            # print(inside_cost_so_far(nei, cost_so_far))
            # if (not inside_cost_so_far(nei, cost_so_far)) or new_cost < cost_so_far[nei]:
            if (not inside_cost_so_far(nei, cost_so_far)) or has_cost_and_is_less_than(nei, new_cost, cost_so_far):
                # cost_so_far[nei] = new_cost
                add_to_cost_so_far(nei, new_cost, cost_so_far)
                priority = new_cost + heuristic(nei)
                frontier.put((priority, nei))
                # came_from[nei] = current
                update_came_from(nei, current, came_from)

    elapsed_time = time.time() - (timeout - MAX_TIMEOUT)

    goal_path: List[PuzzleNode] = []
    current = goal
    while not current.what_am_i.equals(start.what_am_i):
        if current not in came_from:
            goal_path = []
        goal_path.append(current)
        current = came_from[current]

    goal_path.append(start)
    goal_path.reverse()

    return goal_path, visited, elapsed_time


def many_slots_in_correct_place_heuristic(state: PuzzleNode) -> int:
    return state.what_am_i.how_many_incorrect_positions()


def a_star_incorrect_position(puzzle: Puzzle):
    return a_star_search(puzzle, many_slots_in_correct_place_heuristic)


def distance_to_incorrect_heuristic(state: PuzzleNode) -> int:
    return state.what_am_i.how_far_from_correct_positions()


def a_star_distance_to_incorrect(puzzle: Puzzle):
    return a_star_search(puzzle, distance_to_incorrect_heuristic)
