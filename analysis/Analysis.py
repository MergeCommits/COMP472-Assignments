from typing import Tuple, List, Optional

from structures.Puzzle import Puzzle
from structures.PuzzleNode import PuzzleNode

MAX_TIMEOUT = 60


def perform_run(puzzle: Puzzle, algo_function) -> Optional[Tuple[List[PuzzleNode], List[Puzzle], float]]:
    return algo_function(puzzle)


def write_to_file(puzzle: Puzzle, algo_function, filename: str):
    return_tuple = perform_run(puzzle, algo_function)

    with open(filename + "_goal.txt", 'w') as f:
        import sys
        sys.stdout = f  # Change the standard output to the file we created.

        if return_tuple is None:
            print("No solution.")
        else:
            print("GOAL PATH:")
            goal_path = return_tuple[0]
            for element in goal_path:
                element.what_am_i.smart_print()
                print()

    with open(filename + "_search.txt", 'w') as f:
        import sys
        sys.stdout = f  # Change the standard output to the file we created.

        if return_tuple is None:
            print("No solution.")
        else:
            print("SEARCH PATH:")
            visit_path = return_tuple[1]
            for element in visit_path:
                element.smart_print()
                print()


def analyze_20_runs(puzzles: List[Puzzle], algo_function, name: str):
    total_runs = len(puzzles)
    total_goal_path_length = 0
    total_search_path_length = 0
    total_no_solutions = 0
    total_time = float(0)

    for puzzle in puzzles:
        result = perform_run(puzzle, algo_function)
        if result is None:
            total_no_solutions += 1
            total_time += MAX_TIMEOUT
        else:
            total_goal_path_length += len(result[0])
            total_search_path_length += len(result[1])

            elapsed_time = result[2]
            total_time += elapsed_time

    total_solutions = total_runs - total_no_solutions
    if total_solutions == 0:
        total_solutions = 1

    avg_goal_path_length = total_goal_path_length / total_solutions
    avg_search_path_length = total_search_path_length / total_solutions
    avg_time = total_time / total_runs

    print(name)

    print("Average goal path length: " + str(avg_goal_path_length))
    print("Total goal path length: " + str(total_goal_path_length))

    print("Average search path length: " + str(avg_search_path_length))
    print("Total search path length: " + str(total_search_path_length))

    print("Failed runs: " + str(total_no_solutions) + "/" + str(total_runs))

    print("Average runtime: " + str(avg_time))
    print("Total runtime: " + str(total_time))
    print()
    print()

