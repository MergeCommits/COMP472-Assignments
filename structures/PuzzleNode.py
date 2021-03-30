from __future__ import annotations

from typing import List, Optional

from structures.Puzzle import Puzzle


class PuzzleNode:
    what_am_i: Puzzle
    parent: Optional[PuzzleNode]
    children: List[PuzzleNode]

    def __init__(self, uh: Puzzle):
        self.what_am_i = uh
        self.parent = None
        self.children = []

    def search_for_node(self, to_find: Puzzle) -> Optional[PuzzleNode]:
        if self.what_am_i.equals(to_find):
            return self
        else:
            if len(self.children) < 1:
                return None
            else:
                for child in self.children:
                    ret_val = child.search_for_node(to_find)
                    if ret_val is not None:
                        return ret_val

                return None

    def how_deep(self) -> int:
        if self.parent is None:
            return 0
        else:
            total_deepness = 1
            current_node = self.parent
            while current_node.parent is not None:
                total_deepness += 1
                current_node = current_node.parent

            return total_deepness

    def to_travel_list(self) -> List[PuzzleNode]:
        return_list: List[PuzzleNode] = []
        current_node = self

        while True:
            return_list.append(current_node)
            current_node = current_node.parent
            if current_node is None:
                break

        return_list.reverse()
        return return_list

    def __eq__(self, other):
        return 1

    def __hash__(self):
        return hash(self.what_am_i)

