from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for prepositions of time 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  # pattern: as ... as ...
  dep_matcher = DependencyMatcher(nlp.vocab)
  dep_patterns = [
    [
      {
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"POS": "ADP", "LOWER": {"IN": ["in", "on", "between", "at", "for", "since"]}}
      },
      {
        "LEFT_ID": "prep",
        "REL_OP": ">",
        "RIGHT_ID": "time_obj",
        "RIGHT_ATTRS": {"DEP": {"IN": ["pobj"]}, "POS": {"IN": ["NOUN", "PROPN", "NUM"]}}
      },
    ],
  ]
  dep_matcher.add("prep_time", dep_patterns)
  matches = dep_matcher(doc)

  token_ranges = []
  for _, (prep, time_obj) in matches:
    tree = list(doc[time_obj].subtree)
    if any([t.like_num or t.pos_=="NUM" for t in tree]):
      if tree[0].i == prep + 1:
        token_ranges.append((prep, tree[-1].i+1))

  refined_matches = merge(token_ranges)
  s = 0
  for start, end in refined_matches:
    if start > s:
      span = doc[s:start].text
      result.append({"text": span, "highlight": False})
    span = doc[start:end].text
    result.append({"text": span, "highlight": True})
    s = end
  if s < len(doc):
    span = doc[s:].text
    result.append({"text": span, "highlight": False})
 
  return result
