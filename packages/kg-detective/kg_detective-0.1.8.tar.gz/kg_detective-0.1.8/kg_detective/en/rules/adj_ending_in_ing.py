def search_out(doc, nlp):
  """Search for adjective with -ing as its ending

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Token
  """
  _result = [t for t in doc if t.pos_=="ADJ" and t.tag_=="JJ" and len(t.text)>4 and t.text[-3:]=="ing"]

  result = []
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
