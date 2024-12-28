from spacy.matcher import Matcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for comparative adverbs  

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  token_matcher = Matcher(nlp.vocab)
  patterns = [
    [{"POS": "ADV", "OP": "*"}, {"TAG": "RBR"}, {"LOWER": "than", "OP": "?"}],
    [{"POS": "ADV", "OP": "*"}, {"LOWER": "more"}, {"POS": "ADV"}, {"LOWER": "than", "OP": "?"}],
    [{"POS": "ADV", "OP": "*"}, {"TAG": "RBR"}, {"LOWER": "and"}, {"TAG": "RBR"}],
  ]
  token_matcher.add("adv_comparative", patterns)

  matches = token_matcher(doc)
  token_ranges = [(start, end) for _, start, end in matches]

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
