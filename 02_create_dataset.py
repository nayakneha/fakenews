import csv
import os
import pickle
import sys
import fakenews_lib

def main():

  dataset_output_file = sys.argv[1]

  headline_number_map = {}

  headlines_xml_map = {}
  # Read in all headlines (+ parse)

  bodies_xml_map = {}
  # Read in all bodies (+ parse)

  for file_name in os.listdir("/home/nnayak/fakenews/examples/"):
    text_number = os.path.basename(file_name).split('.')[0]

    if file_name.endswith('.body'):
      continue

    with open("/home/nnayak/fakenews/examples/" + file_name, 'r') as f:
      file_text = f.read()

    if file_name.endswith('.headline'):
      headline_number_map[file_text] = text_number
    elif file_name.endswith('.headline.xml'):
      headlines_xml_map[text_number] = file_text
    else:
      assert file_name.endswith('body.xml')
      bodies_xml_map[text_number] = file_text

  # Read in stance dict
  examples = []
  with open("/home/nnayak/other_repos/fnc-1/train_stances.csv") as csv_file:
    stances_reader = csv.reader(csv_file)
    _ = stances_reader.next()
    for row in stances_reader:
      headline, body_id, stance = row
      print stance
      examples.append(fakenews_lib.Example(
        headline_number_map[headline], body_id, stance))

  dataset = fakenews_lib.Dataset(headlines_xml_map, bodies_xml_map, examples)

  with open(dataset_output_file, 'w') as out_file:
    pickle.dump(dataset, out_file)


if __name__ == "__main__":
  main()
