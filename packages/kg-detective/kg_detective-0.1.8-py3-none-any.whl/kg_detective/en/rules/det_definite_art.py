from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for definite article with noun 

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
        "RIGHT_ID": "noun",
        "RIGHT_ATTRS": {"POS":"NOUN"}
      },
      {
        "LEFT_ID": "noun",
        "REL_OP": ">>",
        "RIGHT_ID": "defart",
        "RIGHT_ATTRS": {"POS": "DET", "LEMMA": "the"}
      },
    ],
  ]
  dep_matcher.add("det_definite_art", dep_patterns)
  matches = dep_matcher(doc)

  token_ranges = []
  for _, (noun, defart) in matches:
    noun_tree = [list(e.subtree) for e in doc[noun].lefts]  
    noun_enum = sum(noun_tree, [])
    noun_enum.sort()
    defart_assertion = defart in [e.i for e in noun_enum] 
    noun_assertion = len(noun_enum)>0 and noun_enum[-1].i - noun_enum[0].i + 1 == len(noun_enum) and noun == noun_enum[-1].i + 1
    
    if defart_assertion and noun_assertion:
      token_ranges.append((noun_enum[0].i, noun+1))
  
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
