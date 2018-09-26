import sklearn
import csv
import os

class Label(object):
  UNRELATED='unrelated'
  AGREE='agree'
  DISAGREE='disagree'
  DISCUSS='discuss'

class FileType(object):
  STANCE='stance'
  HEADLINE='headline'
  BODY='body'

ID_hdr = "Body ID"
BODY_hdr = "articleBody"
HEADLINE_hdr = "Headline"
STANCE_hdr = "Stance"

OUTPUT_DIR = "/home/nnayak/fakenews/examples/"

VALID_LABELS = [Label.UNRELATED, Label.AGREE, Label.DISCUSS, Label.DISAGREE]

class Example(object):
  def __init__(self, headline, body, stance, identifier):
    self.headline = headline
    self.body = body
    assert stance in VALID_LABELS
    self.stance = stance
    self.identifier = identifier

def get_file_name(key, file_type):
  key_str = key.zfill(4)
  return "".join([OUTPUT_DIR, key_str, ".", file_type])

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

  file_types = [FileType.STANCE, FileType.HEADLINE, FileType.BODY]

  for key in bodies_dict.keys():
    headline, stance = stances_dict[key]
    for text, file_type in zip([stance, headline, bodies_dict[key]],
        file_types):
      with open(get_file_name(key, file_type), 'w') as f:
        f.write(text)

def main():
  read_data(None)

if __name__ == "__main__":
  main()
