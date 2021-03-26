from typing import List

from Puzzle import Puzzle
from PuzzleNode import PuzzleNode


def run_search(puzzle: Puzzle, algo):
    algo(puzzle)


def was_visited(node: Puzzle, visited: List[Puzzle]) -> bool:
    for visit in visited:
        if node.equals(visit):
            return True

    return False


def dfs_search(puzzle: Puzzle):
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
            this_node = tree_root.search_for_node(node)
            while True:
                this_node.what_am_i.smart_print()
                print()
                this_node = this_node.parent
                if this_node is None:
                    break
            break


def main():
    puz = Puzzle('((4; 3); (2; 1))')
    # puz = Puzzle('((6; 1; 2); (7; 8; 3); (5; 4; 9))')
    # puz = Puzzle('((1; 2; 3; 4); (5; 6; 7; 8); (9; 10; 11; 12); (13; 14; 15; 16))')
    # puz_list = puz.get_permutations()
    # for puzzle in puz_list:
    #     # print(puzzle)
    #     puzzle.smart_print()
    #     print()

    # puz2 = Puzzle('((1; 2; 3); (4; 5; 6); (7; 8; 9))')
    # print(puz.equals(puz2))

    # print(Puzzle('((1; 2; 3; 4); (5; 6; 7; 8); (9; 10; 11; 12); (13; 14; 15; 16))').is_solved())

    run_search(puz, dfs_search)


main()
