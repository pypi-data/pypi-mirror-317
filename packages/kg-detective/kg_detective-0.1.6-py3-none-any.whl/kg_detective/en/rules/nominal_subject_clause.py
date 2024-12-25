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
        "RIGHT_ID": "root",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": "ROOT"},
      },
      {
        "LEFT_ID": "root",
        "REL_OP": ">",
        "RIGHT_ID": "subject_verb",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": "csubj"}
      },
      {
        "LEFT_ID": "subject_verb",
        "REL_OP": ">",
        "RIGHT_ID": "subj",
        "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}, "TAG": {"IN": ["WDT", "WP", "WP$", "WRB"]}}
      },
    ],
  ]
  dep_matcher.add("nominal_subject_clause", dep_patterns)
  matches = dep_matcher(doc)

  token_ranges = []
  for _, (root, verb, _) in matches:
    subj_tree = [e.i for e in doc[verb].subtree]
    subj_tree.sort()

    if len(subj_tree) == subj_tree[-1] - subj_tree[0] + 1:
      token_ranges.append((subj_tree[0], subj_tree[-1]+1)) 

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
