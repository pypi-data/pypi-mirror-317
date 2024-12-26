from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for  

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
        "RIGHT_ID": "copular",
        "RIGHT_ATTRS": {"POS": "AUX", "DEP": "ROOT", "LEMMA": "be"}
      },
      {
        "LEFT_ID": "copular",
        "REL_OP": ">",
        "RIGHT_ID": "predicative",
        "RIGHT_ATTRS": {"DEP": {"IN": ["ccomp", "advcl"]}}
      },
    ],
  ]
  dep_matcher.add("nominal_predicative_clause", dep_patterns)
  matches = dep_matcher(doc)

  token_ranges = []
  for _, (copular, predicative) in matches:
    predicative_tree = [e.i for e in doc[predicative].subtree]
    predicative_tree.sort()

    if len(predicative_tree) == predicative_tree[-1] - predicative_tree[0] + 1:
      token_ranges.append((predicative_tree[0], predicative_tree[-1]+1)) 

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
