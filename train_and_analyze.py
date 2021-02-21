import sklearn
from sklearn.pipeline import Pipeline


def train_model(documents: list, labels: list, pipeline: sklearn.pipeline.Pipeline) -> Pipeline:
    return pipeline.fit(documents, labels)


def predict_eval_data(documents: list, model: sklearn.pipeline.Pipeline) -> list:
    predicted_labels = model.predict(documents)
    return predicted_labels


def return_some_wrong_predictions(all_labels: list, y_train: list, x_test: list, y_truth: list, predicted_labels: list) -> str:
    result_string = ""
    for label in range(len(all_labels)):
        label_name = all_labels[label]
        count = 5

        for i in range(len(predicted_labels)):
            if predicted_labels[i] == label_name and predicted_labels[i] != y_truth[i]:
                row_number = i + len(y_train) + 1
                result_string += f"Line {row_number} wrongly predicted as {label_name}: {x_test[i]}\n"
                count -= 1
                if count == 0:
                    break

    return result_string


def print_to_file(head, report, confusion, wrong_examples, row_predictions, extra=""):
    text_to_write = head
    text_to_write += "\n\nStatistics: \n\n" + report

    text_to_write += "\n\n\nConfusion Matrix: \n\n{}".format(confusion)
    text_to_write += "\n\n\nWrong Prediction Examples: \n\n" + wrong_examples

    if extra:
        text_to_write += "\n\n\nGenerated Decision Tree: \n\n" + extra

    text_to_write += "\n\n\nAll predictions: \n\n" + row_predictions

    print(text_to_write)
