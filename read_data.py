import sklearn
import csv

class Label(object):
  UNRELATED='unrelated'
  AGREE='agree'
  DISAGREE='disagree'
  DISCUSS='discuss'

ID_hdr = "Body ID"
BODY_hdr = "articleBody"
HEADLINE_hdr = "Headline"
STANCE_hdr = "Stance"

VALID_LABELS = [Label.UNRELATED, Label.AGREE, Label.DISCUSS, Label.DISAGREE]

class Example(object):
  def __init__(self, headline, body, stance, identifier):
    self.headline = headline
    self.body = body
    assert stance in VALID_LABELS
    self.stance = stance
    self.identifier = identifier


def read_data(data_path):
  bodies_dict = {}
  with open("/home/nnayak/other_repos/fnc-1/train_bodies.csv") as csv_file:
    article_reader = csv.DictReader(csv_file)
    for row in article_reader:
      print(row)
      bodies_dict[str(row[ID_hdr])] = row[BODY_hdr]

  stances_dict = {}
  with open("/home/nnayak/other_repos/fnc-1/train_stances.csv") as csv_file:
    stance_reader = csv.DictReader(csv_file)
    for row in stance_reader:
      assert row[STANCE_hdr] in VALID_LABELS
      stances_dict[row[ID_hdr]] = (row[HEADLINE_hdr], row[STANCE_hdr])

  examples = []

  for key in bodies_dict.keys():
    headline, stance = stances_dict[key]
    examples.append(Example(headline, bodies_dict[key], stance, key))

  return examples

def featurize(example):
  return example

def featurize_examples(examples):
  return [featurize(example) for example in examples]


def main():
  read_data(None)
  pass

if __name__ == "__main__":
  main()
