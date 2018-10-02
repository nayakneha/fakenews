import os

def main():

  command_line =("java -Xmx5g -cp"
  " \"/home/nnayak/stanford-corenlp-full-2018-02-27/*\""
  " edu.stanford.nlp.pipeline.StanfordCoreNLP -file "
  " \"/home/nnayak/fakenews/examples/{}\""
  " -outputDirectory \"/home/nnayak/fakenews/examples/\"")

  for file_name in os.listdir("/home/nnayak/fakenews/examples/"):
    if file_name.endswith('.headline'):
      print(file_name)
      os.system(command_line.format(file_name))

if __name__ == "__main__":
  main()
