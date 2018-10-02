import pickle
import sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import datasets

import fakenews_lib
import fakenews_features

def sklearn_stuff():
  # import some data to play with
  iris = datasets.load_iris()
  X = iris.data[:, :2]  # we only take the first two features.
  Y = iris.target

  logreg = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')

  # we create an instance of Neighbours Classifier and fit the data.
  logreg.fit(X, Y)

  # cross validation
  scores = cross_val_score(
  clf, iris.data, iris.target, cv=5, scoring='f1_macro')
  # fit
  # predict

def featurize_dataset(dataset, feature_set):

  examples = []
  labels = []

  for example in dataset.examples[:20]:
    try:
      examples.append(fakenews_features.featurize(example, dataset, feature_set))
      labels.append(example.stance)
    except KeyError:
      continue


def main():
  dataset_path = sys.argv[1]
  with open(dataset_path, 'r') as f:
    dataset = pickle.load(f)
  print(dataset)
  featurize_dataset(dataset, fakenews_features.FeatureSets.UNIGRAM_INTERSECTION)

if __name__ == "__main__":
  main()
