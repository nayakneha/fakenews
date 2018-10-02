class FeatureSets(object):
  HEADLINE_UNIGRAMS = "headline_unigrams"
  HEADLINE_BIGRAMS = "headline_bigrams"
  BODY_UNIGRAMS = "body_unigrams"
  BODY_BIGRAMS = "body_bigrams"
  UNIGRAM_INTERSECTION = "unigram_intersection"
  BIGRAM_INTERSECTION = "bigram_intersection"

def tag_features(features, tag):
  return [tag + "$" + feature for feature in features]

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

def bigram_intersection(example):
  intersection = set(bigrams(example.headline_lemmas)).intersection(
          set(bigrams(example.body_lemmas)))
  return list(intersection)

def bigrams(tokens):
  return ["_".join([token1, token2])
        for token1, token2 in zip(tokens[:-1], tokens[1:])]
