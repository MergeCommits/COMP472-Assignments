from __future__ import annotations

import copy
from typing import List


class Puzzle:
    matrix: List[List[int]]
    dim: int

    def __init__(self, representation: str):
        self.matrix = []

        rows = representation[2:-2]
        rows = rows.split('); (')
        for row in rows:
            self.matrix.append(self.__parse_row(row))

        self.dim = len(self.matrix)

    def __parse_row(self, row: str) -> List[int]:
        str_list = row.split(';')
        ret_list = []

        for e in str_list:
            ret_list.append(int(e))

        return ret_list

    def _get_row_permutations(self, row_index: int) -> List[Puzzle]:
        permutes = []

        for i in range(0, self.dim - 1):
            puz_copy = copy.deepcopy(self)
            puz_copy.matrix[row_index][i], puz_copy.matrix[row_index][i + 1] = puz_copy.matrix[row_index][i + 1], \
                                                                               puz_copy.matrix[row_index][i]
            permutes.append(puz_copy)

        return permutes

    def _get_col_permutations(self, row_index) -> List[Puzzle]:
        permutes = []

        for index in range(0, self.dim):
            puz_copy = copy.deepcopy(self)
            puz_copy.matrix[row_index][index], puz_copy.matrix[row_index + 1][index] = puz_copy.matrix[row_index + 1][
                                                                                           index], \
                                                                                       puz_copy.matrix[row_index][index]
            permutes.append(puz_copy)

        return permutes

    def equals(self, other: Puzzle) -> bool:
        n = self.dim * self.dim

        for i in range(0, n):
            x = i // self.dim
            y = i % self.dim

            if self.matrix[x][y] != other.matrix[x][y]:
                return False

        return True

    def get_permutations(self) -> List[Puzzle]:
        permutes = []

        # Get single column permutes first.
        for i in range(0, self.dim):
            permutes = permutes + self._get_row_permutations(i)

        for i in range(0, self.dim - 1):
            permutes = permutes + self._get_col_permutations(i)

        return permutes

    def is_solved(self) -> bool:
        n = self.dim * self.dim

        for i in range(0, n):
            x = i // self.dim
            y = i % self.dim

            if self.matrix[x][y] != (i + 1):
                return False

        return True

    def __str__(self) -> str:
        return_rows = []

        for row in self.matrix:
            str_row = list(map(str, row))
            return_rows.append('(' + '; '.join(str_row) + ')')

        return '(' + '; '.join(return_rows) + ')'

    def smart_print(self):
        for r in self.matrix:
            for c in r:
                print(c, end=" ")
            print()

    def how_many_incorrect_position(self) -> int:
        incorrect_count = 0
        n = self.dim * self.dim

        for i in range(0, n):
            x = i // self.dim
            y = i % self.dim

            if self.matrix[x][y] != (i + 1):
                incorrect_count += 1

        return incorrect_count
