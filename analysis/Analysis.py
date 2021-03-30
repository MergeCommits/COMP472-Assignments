import multiprocessing
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
        # sys.stdout = f  # Change the standard output to the file we created.

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
