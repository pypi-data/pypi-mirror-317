from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for copular verbs   

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """

  result = []

  dep_matcher = DependencyMatcher(nlp.vocab)

  attr_dep = [
    {
      "RIGHT_ID": "core_verb",
      "RIGHT_ATTRS": {"POS": "VERB", "LEMMA": "become"}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "attr",
      "RIGHT_ATTRS": {"DEP": "attr"}
    },
  ]
  acomp_dep = [
    {
      "RIGHT_ID": "core_verb",
      "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "LEMMA": {"IN": ["come", "look", "sound", "taste", "be", "smell", "go", "get", "feel"]}}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "acomp",
      "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "advcl"]}}
    }
  ]

  oprd_dep = [
    {
      "RIGHT_ID": "core_verb",
      "RIGHT_ATTRS": {"POS": {"IN": ["VERB"]}, "LEMMA": {"IN": ["appear"]}}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "oprd",
      "RIGHT_ATTRS": {"DEP": "oprd"}
    }
  ]


  dep_patterns = [attr_dep, acomp_dep, oprd_dep]
  dep_matcher.add("verb_copular", dep_patterns)
  matches = dep_matcher(doc)

  token_ranges = []
  for _, (copular, copular_obj) in matches:
    copular_obj_tree = [e.i for e in doc[copular_obj].subtree]
    copular_obj_tree.sort()

    copular_assertion = copular < copular_obj
    copular_tree_assertion = len(copular_obj_tree) == copular_obj_tree[-1] - copular_obj_tree[0] + 1 
    if copular_assertion and copular_tree_assertion:
      token_ranges.append((copular, copular+1))
      token_ranges.append((copular_obj_tree[0], copular_obj_tree[-1]+1))

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
