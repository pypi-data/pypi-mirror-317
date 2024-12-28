def search_out(doc, nlp):
  """Search for verbs with simple past tense  

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  _result = [t for t in doc if t.tag_ == "VBD" and t.dep_ == "ROOT"]
  s = 0
  for t in _result:
    i = t.i
    if i > s:
      span = doc[s:i].text
      result.append({"text": span, "highlight": False}) 
    result.append({"text": t.text, "highlight": True})
    s = i+1
  if s < len(doc):
    result.append({"text": doc[s:].text, "highlight": False})
  return result
