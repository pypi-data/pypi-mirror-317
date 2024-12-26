from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for prepositions with verb 

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
        "RIGHT_ATTRS": {"POS": "VERB"}
      },
      {
        "LEFT_ID": "verb",
        "REL_OP": ">",
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"DEP": {"IN": ["prep", "prt"]}, "POS": "ADP"}
      },
    ],
  ]
  dep_matcher.add("prep_with_verb", dep_patterns)
  matches = dep_matcher(doc)

  token_ranges = []
  for _, (verb, prep) in matches:
    if prep > verb:
      verb_tree = [list(e.subtree) for e in doc[verb].rights if e.pos_!="PUNCT" and e.dep_ not in ["dep", "cc", "conj"]]
      verb_enum = sum(verb_tree, [])
      if verb_enum[-1].i - verb_enum[0].i == len(verb_enum)-1 and verb == verb_enum[0].i-1:
        token_ranges.append((verb, verb_enum[-1].i+1))

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
