def search_out(doc, nlp):
  """Search for verbs with simple present tense  

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """

  result = []

  _result = [t for t in doc if t.tag_ in ["VBZ", "VBP", "VB"] and t.dep_ == "ROOT" and "Tense=Pres" in t.morph]
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
