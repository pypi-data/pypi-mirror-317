import os
from spacy.matcher import PhraseMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for adverbs of manner 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  pkg_path = os.path.dirname(__file__)
  MANNER = open(pkg_path + '/adv_manner.txt', 'r').read().splitlines() 

  matcher = PhraseMatcher(nlp.vocab)

  patterns = [nlp.make_doc(text) for text in MANNER]
  matcher.add("adv_manner", patterns)

  matches = matcher(doc)
  token_ranges = [(start, end) for _, start, end in matches]

  refined_matches = merge(token_ranges)
  s = 0
  for start, end in refined_matches:
    if start > s:
      span = doc[s:start].text
      result.append({"text": span, "highlight": False})
    span = doc[start:end]
    if any([e.pos_ == "ADV" for e in list(span)]):
      result.append({"text": span.text, "highlight": True})
    else: 
      result.append({"text": span.text, "highlight": False})
    s = end
  if s < len(doc):
    span = doc[s:].text
    result.append({"text": span, "highlight": False})
 
  return result
