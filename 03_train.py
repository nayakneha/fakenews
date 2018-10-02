import pickle
import sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

import fakenews_lib
import fakenews_features

def sklearn_stuff():
  # import some data to play with
  iris = datasets.load_iris()
  X = iris.data[:, :2]  # we only take the first two features.
  Y = iris.target


  # cross validation
  scores = cross_val_score(
  clf, iris.data, iris.target, cv=5, scoring='f1_macro')
  # fit
  # predict

def featurize_dataset(dataset, feature_set):

  examples = []
  labels = []

  for example in dataset.examples:
    examples.append(fakenews_features.featurize(example, dataset, feature_set))
    labels.append(fakenews_lib.STANCES.index(example.stance))

  return examples, np.array(labels)


def main():
  dataset_path = sys.argv[1]
  with open(dataset_path, 'r') as f:
    dataset = pickle.load(f)
  examples, labels = featurize_dataset(dataset,
      [
        #fakenews_features.FeatureSets.UNIGRAM_INTERSECTION,
        fakenews_features.FeatureSets.OPEN_CLASS_INTERSECTION,
        fakenews_features.FeatureSets.HEADLINE_UNIGRAMS])
  vectorizer =  CountVectorizer()
  X = vectorizer.fit_transform(examples)

  logreg = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')
  logreg.fit(X, labels)
  y_pred = logreg.predict(X)
  print(confusion_matrix(logreg.predict(X), labels))
  scores = cross_val_score(logreg, X, labels, cv=10,scoring="f1_macro")
  print(scores)
  print sum(scores)/float(len(scores))


if __name__ == "__main__":
  main()
