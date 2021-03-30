import multiprocessing

from algos.DFS import dfs_search
from algos.ID import id_search
from analysis.Analysis import write_to_file
from structures.Puzzle import Puzzle


def run_search(puzzle: Puzzle, algo):
    algo(puzzle)


def main():
    # puz = Puzzle('((4; 3); (2; 1))')
    puz = Puzzle('((6; 1; 2); (7; 8; 3); (5; 4; 9))')
    # puz = Puzzle('((1; 2; 3; 4); (5; 6; 7; 8); (9; 10; 11; 12); (13; 14; 15; 16))')
    # puz_list = puz.get_permutations()
    # for puzzle in puz_list:
    #     # print(puzzle)
    #     puzzle.smart_print()
    #     print()

    # puz2 = Puzzle('((1; 2; 3); (4; 5; 6); (7; 8; 9))')
    # print(puz.equals(puz2))

    # print(Puzzle('((1; 2; 3; 4); (5; 6; 7; 8); (9; 10; 11; 12); (13; 14; 15; 16))').is_solved())

    # run_search(puz, dfs_search)
    # run_search(puz, id_search)

    if __name__ == '__main__':
        p1 = multiprocessing.Process(target=write_to_file, name="algo", args=(puz, dfs_search, "dfs.txt"))
        p1.start()
        p2 = multiprocessing.Process(target=write_to_file, name="algo", args=(puz, id_search, "id.txt"))
        p2.start()
        p1.join()
        p2.join()
        # write_to_file(puz, dfs_search, "dfs.txt")
        # write_to_file(puz, id_search, "id.txt")


main()
