import time
from multiprocessing import Queue
from typing import List, Optional, Tuple

from analysis.Analysis import MAX_TIMEOUT
from structures.Puzzle import Puzzle
from structures.PuzzleNode import PuzzleNode


def was_visited(node: Puzzle, visited: List[Puzzle]) -> bool:
    for visit in visited:
        if node.equals(visit):
            return True

    return False


def dfs_search(puzzle: Puzzle) -> Optional[Tuple[List[PuzzleNode], List[Puzzle], float]]:
    visited: List[Puzzle] = []
    stack: List[Puzzle] = [puzzle]

    tree_root: PuzzleNode = PuzzleNode(puzzle)

    timeout = time.time() + MAX_TIMEOUT

    while len(stack) > 0:
        if time.time() > timeout:
            return None

        node = stack.pop(0)

        # Have we visited this node before.
        if was_visited(node, visited):
            continue

        if not node.is_solved():
            permutes = node.get_permutations()
            stack = stack + permutes
            visited.append(node)

            current_node = tree_root.search_for_node(node)
            for permutation in permutes:
                new_node = PuzzleNode(permutation)
                new_node.parent = current_node
                current_node.children.append(new_node)
        else:
            elapsed_time = time.time() - (timeout - MAX_TIMEOUT)

            tree_node = tree_root.search_for_node(node)
            print("FINISH")
            return tree_node.to_travel_list(), visited, elapsed_time
