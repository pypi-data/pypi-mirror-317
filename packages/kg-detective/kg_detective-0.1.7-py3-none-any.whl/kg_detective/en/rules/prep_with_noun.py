from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for prepositions with noun 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  dep_matcher = DependencyMatcher(nlp.vocab)
  dep_patterns = [
    [
      {
        "RIGHT_ID": "noun",
        "RIGHT_ATTRS": {"POS": "NOUN"}
      },
      {
        "LEFT_ID": "noun",
        "REL_OP": ">",
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"DEP": "prep", "POS": "ADP"}
      },
      {
        "LEFT_ID": "prep",
        "REL_OP": ">",
        "RIGHT_ID": "prep_obj",
        "RIGHT_ATTRS": {"DEP": "pobj"}
      },
    ],
  ]
  dep_matcher.add("prep_with_noun", dep_patterns)
  matches = dep_matcher(doc)

  token_ranges = []
  for _, (noun, _, _) in matches:
    tree = list(doc[noun].subtree)
    if tree[-1].i - tree[0].i == len(tree)-1:
      token_ranges.append((tree[0].i, tree[-1].i+1))

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
