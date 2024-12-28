from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for intransitive verbs

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []
  black_children_deps = ["dobj", "nsubjpass", "ccomp"]
  black_deps = ["acl"]
  verbs = [t for t in doc if t.pos_=="VERB" and t.dep_ not in black_deps]
   
  token_ranges = []
  for t in verbs:
    deps = [c.dep_ for c in t.children]
    if len(set(deps).intersection(black_children_deps))==0:
      token_ranges.append((t.i, t.i+1))

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
