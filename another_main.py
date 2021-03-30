import multiprocessing
import random
from typing import List

import numpy

from algos.AStar import atar_incorrect_position_heuristic, atar_distance_to_incorrect
from algos.DFS import dfs_search
from algos.ID import id_search
from analysis.Analysis import write_to_file, analyze_20_runs
from structures.Puzzle import Puzzle


def run_search(puzzle: Puzzle, algo):
    algo(puzzle)


def standard_run():
    if __name__ == '__main__':
        # puz = Puzzle('((6; 1; 2); (7; 8; 3); (5; 4; 9))')
        puz = Puzzle('((9; 7; 1); (5; 6; 2); (4; 8; 3))')

        p1 = multiprocessing.Process(target=write_to_file, name="dfs", args=(puz, dfs_search, "dfs.txt"))
        p1.start()
        p2 = multiprocessing.Process(target=write_to_file, name="id", args=(puz, id_search, "id.txt"))
        p2.start()
        p3 = multiprocessing.Process(target=write_to_file, name="astar1",
                                     args=(puz, atar_incorrect_position_heuristic, "astar1.txt"))
        p3.start()
        p4 = multiprocessing.Process(target=write_to_file, name="astar2",
                                     args=(puz, atar_distance_to_incorrect, "astar2.txt"))
        p4.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()


def read_puzzles(filename) -> List[Puzzle]:
    puzzles: List[Puzzle] = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            puzzles.append(Puzzle(line[:-1]))

    return puzzles


def twenty_run():
    if __name__ == '__main__':
        puzzles = read_puzzles("20puzzles.txt")
        analyze_20_runs(puzzles, atar_incorrect_position_heuristic)

        # p1 = multiprocessing.Process(target=write_to_file, name="dfs", args=(puz, dfs_search, "dfs.txt"))
        # p1.start()
        # p2 = multiprocessing.Process(target=write_to_file, name="id", args=(puz, id_search, "id.txt"))
        # p2.start()
        # p3 = multiprocessing.Process(target=write_to_file, name="astar1",
        #                              args=(puz, atar_incorrect_position_heuristic, "astar1.txt"))
        # p3.start()
        # p4 = multiprocessing.Process(target=write_to_file, name="astar2",
        #                              args=(puz, atar_distance_to_incorrect, "astar2.txt"))
        # p4.start()
        #
        # p1.join()
        # p2.join()
        # p3.join()
        # p4.join()


def twenty_generate():
    with open("20puzzles.txt", 'w') as f:
        import sys
        sys.stdout = f  # Change the standard output to the file we created.

        size = 3

        for i in range(20):
            random_list = list(range(1, (size ** 2) + 1))
            random.shuffle(random_list)
            matrix = numpy.array(random_list).reshape([size, size])
            puzzle = Puzzle('((6; 1; 2); (7; 8; 3); (5; 4; 9))')
            puzzle.matrix = matrix
            puzzle.dim = size
            print(puzzle)


def main():
    standard_run()
    # twenty_run()
    # twenty_generate()


main()
