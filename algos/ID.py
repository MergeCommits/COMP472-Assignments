import time
from multiprocessing import Queue
from typing import List, Optional, Tuple

from analysis.Analysis import MAX_TIMEOUT
from structures.Puzzle import Puzzle
from structures.PuzzleNode import PuzzleNode
from algos.DFS import was_visited


def dfs_max_depth_search(puzzle: Puzzle, max_depth: int, timeout: float) -> Optional[Tuple[List[PuzzleNode], List[Puzzle]]]:
    visited: List[Puzzle] = []
    stack: List[Puzzle] = [puzzle]

    tree_root: PuzzleNode = PuzzleNode(puzzle)

    while len(stack) > 0:
        if time.time() > timeout:
            return None

        node = stack.pop(0)

        # Have we visited this node before.
        if was_visited(node, visited):
            continue

        if not node.is_solved():
            current_node = tree_root.search_for_node(node)
            if current_node.how_deep() <= max_depth:
                permutes = node.get_permutations()
                stack = stack + permutes
                visited.append(node)

                for permutation in permutes:
                    new_node = PuzzleNode(permutation)
                    new_node.parent = current_node
                    current_node.children.append(new_node)
        else:
            this_node = tree_root.search_for_node(node)
            return this_node.to_travel_list(), visited

    return None


def id_search(puzzle: Puzzle) -> Optional[Tuple[List[PuzzleNode], List[Puzzle], float]]:
    max_depth = 0
    goal_result: Optional[PuzzleNode] = None

    timeout = time.time() + MAX_TIMEOUT

    while goal_result is None:
        if time.time() > timeout:
            return None

        max_depth += 1
        goal_result = dfs_max_depth_search(puzzle, max_depth, timeout)
