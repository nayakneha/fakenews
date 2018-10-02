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
      bodies_dict[str(row[ID_hdr])] = row[BODY_hdr]

  headlines = set()
  with open("/home/nnayak/other_repos/fnc-1/train_stances.csv") as csv_file:
    stance_reader = csv.reader(csv_file)
    for i, row in enumerate(stance_reader):
      headline, body_id, stance = row
      headlines.add(headline)

  headline_list = sorted(list(headlines))
  headline_map = { headline: str(headline_list.index(headline)).zfill(4)
                   for headline in headline_list}

  with open("/home/nnayak/other_repos/fnc-1/headline_map.csv",
         'w') as output_csv_file:
   headline_writer = csv.writer(output_csv_file)
   for headline, headline_id in headline_map.iteritems():
     headline_writer.writerow([headline, headline_id])


   with open("/home/nnayak/other_repos/fnc-1/train_stances.csv") as csv_file:
     stance_reader = csv.reader(csv_file)
     for i, row in enumerate(stance_reader):
       headline, body_id, stance = row
       headline_id = headline_map[headline]
       with open(get_file_name(headline_id, FileType.HEADLINE), 'w') as f:
         f.write(headline)

  file_types = [FileType.STANCE, FileType.HEADLINE, FileType.BODY]

  #for key in bodies_dict.keys():
  #  headline, stance = stances_dict[key]
  #  for text, file_type in zip([stance, headline, bodies_dict[key]],
  #      file_types):
  #    with open(get_file_name(key, file_type), 'w') as f:
  #      f.write(text)

def main():
  read_data(None)

if __name__ == "__main__":
  main()
