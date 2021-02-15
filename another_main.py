from __future__ import division

from codecs import open

import sklearn
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier


def read_documents(doc_file):
    docs = []
    labels = []
    with open(doc_file, encoding='utf-8') as f:
        for line in f:
            separation = line.split(' ', 3)
            labels.append(separation[1])
            docs.append(separation[3])
    return docs, labels


def train_model(documents: list, labels: list, pipeline: sklearn.pipeline.Pipeline) -> Pipeline:
    return pipeline.fit(documents, labels)


def predict_eval_data(documents: list, labels: list, model: sklearn.pipeline.Pipeline):
    predicted_labels = model.predict(documents)

    target_labels = [labels[0], "pos" if labels[0] == "neg" else "neg"]

    print(metrics.classification_report(labels, predicted_labels, labels=target_labels))
    print(metrics.confusion_matrix(labels, predicted_labels))


def run_train_and_analyze(pipeline: sklearn.pipeline.Pipeline,
                          x_train: list,
                          y_train: list,
                          x_test: list,
                          y_truth: list,
                          filename: str):
    with open(filename, 'w') as f:
        import sys
        # sys.stdout = f  # Change the standard output to the file we created.
        ml_model = train_model(x_train, y_train, pipeline)
        predict_eval_data(x_test, y_truth, ml_model)


naive_bayes_pipeline = Pipeline([
    ('vec', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB(alpha=0.0)),
])

base_dt_pipeline = Pipeline([
    ('vec', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', DecisionTreeClassifier(criterion="entropy", splitter="random")),
])

tree_para = {'criterion': ['gini', 'entropy'],
             'max_depth': [4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20, 30, 40, 50, 70, 90, 120, 150]}

clf = GridSearchCV(DecisionTreeClassifier(), tree_para, cv=5)
best_dt_pipeline = Pipeline([
    ('vec', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', DecisionTreeClassifier(criterion="entropy", splitter="best"))
    # ('clf', GridSearchCV(DecisionTreeClassifier, tree_para, cv=5))
])

all_docs, all_labels = read_documents("all_sentiment_shuffled.txt")
split_point = int(0.80 * len(all_docs))
train_docs = all_docs[:split_point]
train_labels = all_labels[:split_point]
eval_docs = all_docs[split_point:]
eval_labels = all_labels[split_point:]

run_train_and_analyze(naive_bayes_pipeline,
                      train_docs,
                      train_labels,
                      eval_docs,
                      eval_labels,
                      "nb-reviews.txt")

run_train_and_analyze(base_dt_pipeline,
                      train_docs,
                      train_labels,
                      eval_docs,
                      eval_labels,
                      "basedt-reviews.txt")

run_train_and_analyze(best_dt_pipeline,
                      train_docs,
                      train_labels,
                      eval_docs,
                      eval_labels,
                      "bestdt-reviews.txt")
