def search_out(doc, nlp):
  """Search for interrogative pronouns 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Token
  """


  _result = [t for t in doc if t.pos_ in ["PRON", "DET"] and t.tag_ in ["WDT", "WP", "WP$", "WRB"]]

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
