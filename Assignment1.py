import sklearn
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import metrics
from sklearn import tree
import numpy
from collections import Counter
import matplotlib

SPLIT_PERCENT = 0.8
DOCUMENT_NAME = "all_sentiment_shuffled.txt"
NAIVESBAYES_SMOOTHING = 1

label_list = []
training_labels = []
training_data = []
eval_labels = []
eval_data = []

def main():
    global label_list, training_labels, training_data, eval_labels, eval_data

    document = read_document(DOCUMENT_NAME)

    split_point = int(SPLIT_PERCENT*len(document))

    training_label_names, training_data = separate_doc_fields(document[:split_point])
    eval_label_names, eval_data = separate_doc_fields(document[split_point:])
    label_list = get_labels(training_label_names)

    training_labels = label_to_index(training_label_names)
    eval_labels = label_to_index(eval_label_names)

    naivesBayes()
    baseDecisionTree()
    bestDecisionTree()

def read_document(file):
    f = open(file, "r", encoding="utf-8")
    document = f.readlines()
    return document

def separate_doc_fields(documents):
    labels = []
    docs = []

    for line in documents:
        separation = line.split(' ', 3)
        labels.append(separation[1])
        docs.append(separation[3])

    return labels, docs

def get_labels(labels):
    label_list = []
    for label in labels:
        if label not in label_list:
            label_list.append(label)

    return label_list

def separate_by_label(label_list, labels, documents):
    document_separation = []

    for i in label_list:
        document_separation.append([])

    for i in range(len(documents)):
        index = label_list.index(labels[i])
        document_separation[index].append(documents[i])

    return document_separation

def count_words(documents):
    frequencies = Counter()

    for doc in documents:
        split_doc = doc.split()
        frequencies.update(split_doc)

    return frequencies

def label_to_index(labels):
    print(label_list)
    label_index = []
    for label in labels:
        label_index.append(label_list.index(label))

    return label_index


def naivesBayes():

    text_classifier = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB(alpha=NAIVESBAYES_SMOOTHING))
    ])

    text_classifier.fit(training_data, training_labels)

    predicted = text_classifier.predict(eval_data)

    statistics = metrics.classification_report(eval_labels, predicted, target_names=label_list)

    confusion = metrics.confusion_matrix(eval_labels, predicted)

    wrongExamples = returnSomeWrongPredictions(predicted)

    printToFile("NaivesBayes.txt", "Naives Bayes Classifier", statistics, confusion, wrongExamples)

def baseDecisionTree():

    text_classifier = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', tree.DecisionTreeClassifier(criterion="entropy", splitter="random"))
    ])

    text_classifier.fit(training_data, training_labels)

    predicted = text_classifier.predict(eval_data)

    statistics = metrics.classification_report(eval_labels, predicted, target_names=label_list)

    confusion = metrics.confusion_matrix(eval_labels, predicted)

    text_classifier["vect"]._validate_vocabulary()
    generatedTree = tree.export_text(text_classifier["clf"], feature_names=text_classifier["vect"].get_feature_names())

    wrongExamples = returnSomeWrongPredictions(predicted)

    printToFile("BaseDT.txt", "Base Decision Tree", statistics, confusion, wrongExamples, generatedTree)

def bestDecisionTree():

    text_classifier = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', tree.DecisionTreeClassifier(criterion="gini", splitter="best", min_impurity_decrease=0.0005))
    ])


    text_classifier.fit(training_data, training_labels)

    predicted = text_classifier.predict(eval_data)

    statistics = metrics.classification_report(eval_labels, predicted, target_names=label_list)

    confusion = metrics.confusion_matrix(eval_labels, predicted)

    text_classifier["vect"]._validate_vocabulary()
    generatedTree = tree.export_text(text_classifier["clf"], feature_names=text_classifier["vect"].get_feature_names())

    wrongExamples = returnSomeWrongPredictions(predicted)

    printToFile("BestDT.txt", "Best Decision Tree", statistics, confusion, wrongExamples, generatedTree)

def returnSomeWrongPredictions(prediction):
    result_string = ""
    for label in range(len(label_list)):
        count = 5
        for i in range(len(prediction)):
            if prediction[i] == label and prediction[i] != eval_labels[i]:
                result_string += f"Line {i+len(training_labels)+1} wrongly predicted as {label_list[label]}: {eval_data[i]}\n"
                count -= 1
                if count == 0:
                    break

    return result_string


def printToFile(fileName, head, statistics, confusion, wrongExamples, extra=""):
    textToWrite = head
    textToWrite += "\n\nStatistics: \n\n" + statistics
    print(confusion)
    textToWrite += "\n\n\nConfusion Matrix: \n\n{}".format(confusion)
    textToWrite += "\n\n\nWrong Prediction Examples: \n\n" + wrongExamples
    if extra:
        textToWrite += "\n\n\nGenerated Decision Tree: \n\n" + extra

    file = open(fileName, "w")
    file.write(textToWrite)
    file.close()

main()