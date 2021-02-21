from base_tree import base_decision_tree


def best_decision_tree(x_train: list,
                       y_train: list,
                       x_test: list,
                       y_truth: list,
                       all_labels: list):
    base_decision_tree(x_train, y_train, x_test, y_truth, all_labels, best_parameters=True)
