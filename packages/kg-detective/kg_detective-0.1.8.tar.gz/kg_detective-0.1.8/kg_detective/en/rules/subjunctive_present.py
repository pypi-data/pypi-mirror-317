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
        "RIGHT_ID": "core_verb",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": "ROOT", "TAG": "VB"}
      },
      {
        "LEFT_ID": "core_verb",
        "REL_OP": ">",
        "RIGHT_ID": "advcl_verb",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": "advcl", "TAG": "VBD"}
      },
      {
        "LEFT_ID": "core_verb",
        "REL_OP": ">",
        "RIGHT_ID": "aux_core",
        "RIGHT_ATTRS": {"POS": "AUX", "DEP": "aux", "TAG": "MD"}
      },
    ],
  ]
  dep_matcher.add("subjunctive_present", dep_patterns)
  matches = dep_matcher(doc)

  token_ranges = []
  for _, (core_verb, advcl_verb, aux_core) in matches:
    clause_tree = [e.i for e in doc[advcl_verb].subtree]
    clause_tree.sort()

    verb_assertion = aux_core < core_verb
    clause_assertion = len(clause_tree) == clause_tree[-1] - clause_tree[0] + 1
  
    if verb_assertion and clause_assertion:
      token_ranges.append((aux_core, core_verb+1))
      token_ranges.append((clause_tree[0], clause_tree[-1]+1))

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
 
