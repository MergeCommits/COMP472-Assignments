import multiprocessing
import random
from typing import List

import numpy

from algos.AStar import a_star_incorrect_position, a_star_distance_to_incorrect
from algos.DFS import dfs_search
from algos.ID import id_search
from analysis.Analysis import write_to_file, analyze_20_runs
from structures.Puzzle import Puzzle


def run_search(puzzle: Puzzle, algo):
    algo(puzzle)


def standard_run():
    if __name__ == '__main__':
        puz = Puzzle('((8; 3; 4); (6; 2; 5); (7; 1; 9))')
        # puz = Puzzle('((9; 12; 1; 3); (14; 11; 10; 8); (13; 6; 5; 15); (7; 2; 16; 4))')

        p1 = multiprocessing.Process(target=write_to_file, name="dfs", args=(puz, dfs_search, "dfs"))
        p1.start()
        p2 = multiprocessing.Process(target=write_to_file, name="id", args=(puz, id_search, "id"))
        p2.start()
        p3 = multiprocessing.Process(target=write_to_file, name="astar1",
                                     args=(puz, a_star_incorrect_position, "astar1"))
        p3.start()
        p4 = multiprocessing.Process(target=write_to_file, name="astar2",
                                     args=(puz, a_star_distance_to_incorrect, "astar2"))
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
        # analyze_20_runs(puzzles, a_star_distance_to_incorrect)

        p1 = multiprocessing.Process(target=analyze_20_runs, name="dfs", args=(puzzles, dfs_search, "Depth-first search"))
        p1.start()
        p2 = multiprocessing.Process(target=analyze_20_runs, name="id", args=(puzzles, id_search, "Iterative deepening"))
        p2.start()
        p3 = multiprocessing.Process(target=analyze_20_runs, name="astar1",
                                     args=(puzzles, a_star_incorrect_position, "AStar 1"))
        p3.start()
        p4 = multiprocessing.Process(target=analyze_20_runs, name="astar2",
                                     args=(puzzles, a_star_distance_to_incorrect, "AStar 2"))
        p4.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()


def twenty_generate():
    with open("20puzzles.txt", 'w') as f:
        import sys
        sys.stdout = f  # Change the standard output to the file we created.

        size = 4

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
