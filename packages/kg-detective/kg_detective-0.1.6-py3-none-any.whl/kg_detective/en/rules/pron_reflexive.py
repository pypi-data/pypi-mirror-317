import os
def search_out(doc, nlp):
  """Search for reflexive pronouns 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Token
  """

  pkg_path = os.path.dirname(__file__)
  REFLEXIVE = open(pkg_path + '/pron_reflexive.txt', 'r').read().splitlines() 

  _result = [t for t in doc if t.text.lower() in REFLEXIVE]

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
