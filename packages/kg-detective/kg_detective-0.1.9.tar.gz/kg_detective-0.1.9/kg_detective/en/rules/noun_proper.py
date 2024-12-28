from spacy.matcher import Matcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for proper nouns 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """

  result = []

  matcher = Matcher(nlp.vocab)
  patterns = [
    [{"POS": "DET", "OP": "?"}, {"POS": "PROPN", "OP": "+"}],
    [{"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": "PART", "TAG": "POS", "OP": "+"}, {"POS": "PROPN"}]
  ]
  matcher.add("noun_proper", patterns)

  matches = matcher(doc)
  ranges = [(start, end) for _, start, end in matches]
  refined_matches = merge(ranges)
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
