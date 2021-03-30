import multiprocessing
import time
from typing import Tuple, List, Optional

from structures.Puzzle import Puzzle
from structures.PuzzleNode import PuzzleNode

MAX_TIMEOUT = 60


def perform_run(puzzle: Puzzle, algo_function) -> Optional[Tuple[List[PuzzleNode], List[Puzzle]]]:
    pro_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=algo_function, name="algo", args=(puzzle, pro_queue))
    p.start()

    p.join(MAX_TIMEOUT)

    if p.is_alive():
        p.terminate()
        p.join()

        return None

    return pro_queue.get()


def write_to_file(puzzle: Puzzle, algo_function, filename: str):
    with open(filename, 'w') as f:
        import sys
        sys.stdout = f  # Change the standard output to the file we created.

        return_tuple = perform_run(puzzle, algo_function)

        if return_tuple is None:
            print("No solution.")
            return

        print("GOAL PATH:")
        goal_path = return_tuple[0]
        for element in goal_path:
            element.what_am_i.smart_print()
            print()

        print("SEARCH PATH:")
        visit_path = return_tuple[1]
        for element in visit_path:
            element.smart_print()
            print()


def analyze_20_runs(puzzles: List[Puzzle], algo_function):
    total_runs = len(puzzles)
    total_goal_path_length = 0
    total_search_path_length = 0
    total_no_solutions = 0
    total_time = float(0)

    for puzzle in puzzles:
        start_time = time.time()
        result = perform_run(puzzle, algo_function)
        if result is None:
            total_no_solutions += 1
            total_time += 60
        else:
            end_time = time.time()

            total_goal_path_length += len(result[0])
            total_search_path_length += len(result[1])

            elapsed_time = end_time - start_time
            total_time += elapsed_time

    avg_goal_path_length = total_goal_path_length / total_runs
    avg_search_path_length = total_search_path_length / total_runs
    avg_time = total_time / total_runs

    print("Average goal path length: " + str(avg_goal_path_length))
    print("Total goal path length: " + str(total_goal_path_length))

    print("Average search path length: " + str(avg_search_path_length))
    print("Total search path length: " + str(total_search_path_length))

    print("Failed runs: " + str(total_no_solutions) + "/" + str(total_runs))

    print("Average runtime: " + str(avg_time))
    print("Total runtime: " + str(total_time))

