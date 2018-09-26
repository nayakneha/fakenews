def main():
  for event, elem in ET.iterparse(
      '/home/nnayak/fakenews/examples/0000.headline.xml'):
    sentences = []
    if elem.tag == "sentence":
      k = Example(elem)


if __name__=="__main__":
  main()
