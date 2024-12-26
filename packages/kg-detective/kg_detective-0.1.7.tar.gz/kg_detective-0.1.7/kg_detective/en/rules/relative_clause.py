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
        "RIGHT_ID": "noun",
        "RIGHT_ATTRS": {"POS": "NOUN"}
      },
      {
        "LEFT_ID": "noun",
        "REL_OP": ">",
        "RIGHT_ID": "clause",
        "RIGHT_ATTRS": {"DEP": "relcl"}
      },
    ],
  ]
  dep_matcher.add("relative_clause", dep_patterns)
  matches = dep_matcher(doc)

  token_ranges = []
  for _, (noun, clause) in matches:
    whole_noun_tree = [e.i for e in doc[noun].subtree]
    clause_tree = [e.i for e in doc[clause].subtree]
  
    noun_tree = list(set(whole_noun_tree) - set(clause_tree))

    noun_tree.sort()
    clause_tree.sort()

    noun_assertion = len(noun_tree) == noun_tree[-1] - noun_tree[0] + 1
    clause_assertion = len(clause_tree) == clause_tree[-1] - clause_tree[0] + 1

    if noun_assertion and clause_assertion:
      token_ranges.append((noun_tree[0], noun_tree[-1]+1))
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
   
