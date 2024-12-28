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
        "RIGHT_ID": "verb",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": {"IN": ["ROOT", "xcomp"]}, "LEMMA": {"NOT_IN": ["be"]}}
      },
      {
        "LEFT_ID": "verb",
        "REL_OP": ">",
        "RIGHT_ID": "obj",
        "RIGHT_ATTRS": {"DEP": "ccomp"}
      },
    ],
  ]
  dep_matcher.add("nominal_object_clause", dep_patterns)
  matches = dep_matcher(doc)

  token_ranges = []
  for _, (verb, obj) in matches:
    obj_tree = [e.i for e in doc[obj].subtree]
    obj_tree.sort()

    if len(obj_tree) == obj_tree[-1] - obj_tree[0] + 1:
      token_ranges.append((obj_tree[0], obj_tree[-1]+1)) 

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
