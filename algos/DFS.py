from multiprocessing import Queue
from typing import List

from structures.Puzzle import Puzzle
from structures.PuzzleNode import PuzzleNode


def was_visited(node: Puzzle, visited: List[Puzzle]) -> bool:
    for visit in visited:
        if node.equals(visit):
            return True

    return False


def dfs_search(puzzle: Puzzle, queue: Queue):
    visited: List[Puzzle] = []
    stack: List[Puzzle] = [puzzle]

    tree_root: PuzzleNode = PuzzleNode(puzzle)

    while len(stack) > 0:
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
            tree_node = tree_root.search_for_node(node)
            queue.put((tree_node, visited))
            break
