from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for transitive verbs   

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """

  result = []

  dep_matcher = DependencyMatcher(nlp.vocab)

  verb_phrase = [
    {
      "RIGHT_ID": "core_verb",
      "RIGHT_ATTRS": {"POS": "VERB"}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "dobj",
      "RIGHT_ATTRS": {"DEP": {"IN": ["dobj", "nsubjpass"]}}
    },
  ]

  dep_patterns = [verb_phrase]
  dep_matcher.add("verb_transitive", dep_patterns)
  matches = dep_matcher(doc)

  token_ranges = []
  for _, (verb, obj) in matches:
    tree = list(doc[obj].subtree)
    if verb < obj and tree[-1].i - tree[0].i == len(tree)-1:
      token_ranges.append((verb, tree[-1].i+1))

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
   
