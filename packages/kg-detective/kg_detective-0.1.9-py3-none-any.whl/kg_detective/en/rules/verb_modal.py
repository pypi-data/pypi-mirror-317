from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for verbs with verb modal   

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed

  Returns:
    list: list of spacy.tokens.Span
  """

  result = []

  token_ranges = [(t.i, t.i+1) for t in doc if t.tag_=="MD"]

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
