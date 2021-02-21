from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from train_and_analyze import train_model, predict_eval_data, return_some_wrong_predictions, print_to_file

NAIVES_BAYES_SMOOTHING = float(1)


def naive_bayes(x_train: list,
                y_train: list,
                x_test: list,
                y_truth: list,
                all_labels: list):
    naive_bayes_pipeline = Pipeline([
        ('vec', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB(alpha=NAIVES_BAYES_SMOOTHING)),
    ])

    with open("nb-reviews.txt", 'w') as f:
        import sys
        sys.stdout = f  # Change the standard output to the file we created.
        ml_model = train_model(x_train, y_train, naive_bayes_pipeline)
        predicted_labels = predict_eval_data(x_test, ml_model)

        report = metrics.classification_report(y_truth, predicted_labels, labels=all_labels)
        confusion_matrix = metrics.confusion_matrix(y_truth, predicted_labels)
        wrong_predictions = return_some_wrong_predictions(all_labels, y_train, x_test, y_truth, predicted_labels)

        row_predictions = ""
        for i in range(len(predicted_labels)):
            row_predictions += f'Row #{i + 1} predicts {predicted_labels[i]}\n'

        print_to_file("Naives Bayes Classifier", report, confusion_matrix, wrong_predictions, row_predictions)
