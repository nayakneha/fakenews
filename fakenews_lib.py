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
  def __init__(self, headline, body_xml):
    self.headline = Sentence(headline)
    self.body = [Sentence(sentence_xml) for sentence_xml in body_xml]
    self.headline_lemmas = self.headline.token_map["lemma"]
    self.body_lemmas = sum([sentence.token_map["lemma"]
                            for sentence in self.body], [])

class FeatureSets(object):
  HEADLINE_UNIGRAMS = "headline_unigrams"
  HEADLINE_BIGRAMS = "headline_bigrams"
  BODY_UNIGRAMS = "body_unigrams"
  BODY_BIGRAMS = "body_bigrams"
  UNIGRAM_INTERSECTION = "unigram_intersection"
  BIGRAM_INTERSECTION = "bigram_intersection"

def tag_features(features, tag):
  return [tag + "_" + feature for feature in features]

def featurize(example, feature_set):
  features = []

  if FeatureSets.HEADLINE_UNIGRAMS in feature_set:
    features += tag_features(example.headline_lemmas,
        FeatureSets.HEADLINE_UNIGRAMS))

  if FeatureSets.HEADLINE_BIGRAMS in feature_set:
    features += tag_features(bigrams(example.headline_lemmas),
        FeatureSets.HEADLINE_BIGRAMS))

  if FeatureSets.BODY_UNIGRAMS in feature_set:
    features += tag_features(example.body_lemmas,
        FeatureSets.BODY_UNIGRAMS))

  if FeatureSets.BODY_BIGRAMS in feature_set:
    features += tag_features(bigrams(example.body_lemmas),
        FeatureSets.BODY_BIGRAMS))

  if FeatureSets.UNIGRAM_INTERSECTION in feature_set:
    features += tag_features(unigram_intersection(example),
        FeatureSets.UNIGRAM_INTERSECTION)

  if FeatureSets.BIGRAM_INTERSECTION in feature_set:
    features += tag_features(bigram_intersection(example),
        FeatureSets.BIGRAM_INTERSECTION)

 return features

def unigram_intersection(example):
  intersection =
  set(example.headline_lemmas).intersection(set(example.body_lemmas))
  return list(intersection)

def unigram_intersection(example):
  intersection = set(bigrams(example.headline_lemmas)).intersection(
          set(bigrams(example.body_lemmas)))
  return list(intersection)

def bigrams(tokens):
  return ["_".join([token1, token2])
        for token1, token2 in zip(tokens[:-1], tokens[1:])]
