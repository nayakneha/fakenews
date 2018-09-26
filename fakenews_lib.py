import collections
import lxml.etree as ET

REQUIRED_TAGS = ['word', 'lemma', 'POS']

class DependencyNode(object):
  def __init__(self, idx, text, governor_idx, dep_type):
    self.idx = idx
    self.text = text
    self.governor_idx= governor_idx
    self.dep_type = dep_type
    self.children = []

class DependencyParse(object):
  def __init__(self):
    root_node = DependencyNode("0", "ROOT", "-1", "None")
    self.nodes = {"0":root_node}
    pass

  def add_dependency(self, dependency):
    assert dependency.tag == "dep"
    for child in dependency:
      if child.tag == "governor":
        governor_idx = child.get("idx")
      else:
        assert child.tag == "dependent"
        dependent_idx = child.attrib["idx"]
        dependent_text = child.text
    self.nodes[dependent_idx] = DependencyNode(dependent_idx, dependent_text,
        governor_idx, dependency.attrib["type"])

  def assemble_tree(self):
    for idx, node in self.nodes.iteritems():
      if idx == "0":
        continue
      self.nodes[node.governor_idx].children.append((node.dep_type, node))


class Sentence(object):
  def __init__(self, xml_sentence):
    assert xml_sentence.tag == "sentence"

    self.dependency_parse = DependencyParse()

    for elem in xml_sentence:
      if elem.tag == "tokens":
        self.tokens = self.add_tokens(elem)
      else:
        assert elem.tag == "dependencies"
        print(ET.tostring(elem, pretty_print=True))
        for dep in elem:
          self.dependency_parse.add_dependency(dep)
    self.dependency_parse.assemble_tree()

  def add_tokens(self, tokens):
    tag_lists = collections.defaultdict(list)
    for token in tokens:
      for child in token:
        if child.tag in REQUIRED_TAGS:
          tag_lists[child.tag].append(child.text)
    return tag_lists


class Example(object):
  def __init__(self, headline):
    self.headline = Sentence(headline)
    pass


