from __future__ import division

from codecs import open

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from base_tree import base_decision_tree
from best_tree import best_decision_tree
from naive_bayes import naive_bayes

SPLIT_PERCENT = 0.8
DOCUMENT_NAME = "all_sentiment_shuffled.txt"


def read_documents(doc_file):
    docs = []
    labels = []
    with open(doc_file, encoding='utf-8') as f:
        for line in f:
            separation = line.split(' ', 3)
            labels.append(separation[1])
            docs.append(separation[3])
    return docs, labels


def get_labels(labels):
    label_list = []
    for label in labels:
        if label not in label_list:
            label_list.append(label)

    return label_list


def main():
    all_docs, all_labels = read_documents(DOCUMENT_NAME)
    split_point = int(SPLIT_PERCENT * len(all_docs))

    train_docs = all_docs[:split_point]
    train_labels = all_labels[:split_point]

    eval_docs = all_docs[split_point:]
    eval_labels = all_labels[split_point:]

    all_labels = get_labels(train_labels)

    naive_bayes(train_docs,
                train_labels,
                eval_docs,
                eval_labels,
                all_labels)

    base_decision_tree(train_docs,
                       train_labels,
                       eval_docs,
                       eval_labels,
                       all_labels)

    best_decision_tree(train_docs,
                       train_labels,
                       eval_docs,
                       eval_labels,
                       all_labels)


main()
