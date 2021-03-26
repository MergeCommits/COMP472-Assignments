from __future__ import annotations

from typing import List, Optional

from Puzzle import Puzzle


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
