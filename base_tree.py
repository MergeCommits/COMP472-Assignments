from sklearn import metrics
from sklearn import tree
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.tree import DecisionTreeClassifier

from train_and_analyze import train_model, predict_eval_data, return_some_wrong_predictions, print_to_file


def base_decision_tree(x_train: list,
                       y_train: list,
                       x_test: list,
                       y_truth: list,
                       all_labels: list,
                       best_parameters=False):
    dt_clf = DecisionTreeClassifier(criterion="entropy", splitter="random") if best_parameters else DecisionTreeClassifier(criterion="entropy")

    base_dt_pipeline = Pipeline([
        ('vec', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', dt_clf),
    ])

    file_name = "bestdt-reviews.txt" if best_parameters else "basedt-reviews.txt"
    with open(file_name, 'w') as f:
        import sys
        sys.stdout = f  # Change the standard output to the file we created.
        ml_model = train_model(x_train, y_train, base_dt_pipeline)
        predicted_labels = predict_eval_data(x_test, ml_model)

        report = metrics.classification_report(y_truth, predicted_labels, labels=all_labels)
        confusion_matrix = metrics.confusion_matrix(y_truth, predicted_labels)
        wrong_predictions = return_some_wrong_predictions(all_labels, y_train, x_test, y_truth, predicted_labels)

        base_dt_pipeline["vec"]._validate_vocabulary()
        generated_tree = tree.export_text(base_dt_pipeline["clf"],
                                          feature_names=base_dt_pipeline["vec"].get_feature_names(),
                                          max_depth=5)

        row_predictions = ""
        for i in range(len(predicted_labels)):
            row_predictions += f'Row #{i + 1} predicts {predicted_labels[i]}\n'

        title = "Best Decision Tree" if best_parameters else "Base Decision Tree"
        print_to_file(title, report, confusion_matrix, wrong_predictions, row_predictions,
                      generated_tree)
