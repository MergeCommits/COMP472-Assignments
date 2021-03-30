from multiprocessing import Queue
from typing import List, Optional, Tuple

from structures.Puzzle import Puzzle
from structures.PuzzleNode import PuzzleNode
from algos.DFS import was_visited


def dfs_max_depth_search(puzzle: Puzzle, max_depth: int, queue: Queue) -> Optional[PuzzleNode]:
    visited: List[Puzzle] = []
    stack: List[Puzzle] = [puzzle]

    tree_root: PuzzleNode = PuzzleNode(puzzle)

    while len(stack) > 0:
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
            queue.put((this_node.to_travel_list(), visited))
            return this_node

    return None


def id_search(puzzle: Puzzle, queue: Queue):
    max_depth = 0
    goal_node: Optional[PuzzleNode] = None

    while goal_node is None:
        max_depth += 1
        goal_node = dfs_max_depth_search(puzzle, max_depth, queue)

    # this_node = goal_node
    # print("MAX DEPTH WAS: " + str(max_depth))
    # print("DEPTH WAS: " + str(this_node.how_deep()))
    # while True:
    #     this_node.what_am_i.smart_print()
    #     print()
    #     this_node = this_node.parent
    #     if this_node is None:
    #         break
