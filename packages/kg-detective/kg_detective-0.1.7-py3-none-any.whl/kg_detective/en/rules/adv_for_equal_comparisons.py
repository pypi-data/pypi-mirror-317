from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for adverbs for equal comparisons 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  # pattern: as ... as ...
  dep_matcher = DependencyMatcher(nlp.vocab)
  dep_patterns = [
    [
      {
        "RIGHT_ID": "A",
        "RIGHT_ATTRS": {"POS": "ADV"}
      },
      {
        "LEFT_ID": "A",
        "REL_OP": ">",
        "RIGHT_ID": "left_as",
        "RIGHT_ATTRS": {"DEP": "advmod", "LOWER": {"IN": ["as", "so"]}}
      },
      {
        "LEFT_ID": "A",
        "REL_OP": ".",
        "RIGHT_ID": "right_as",
        "RIGHT_ATTRS": {"POS": {"IN": ["ADP", "SCONJ"]}, "LOWER": "as"}
      },
    ],
  ]
  dep_matcher.add("adv_equal_comprison", dep_patterns)
  matches = dep_matcher(doc)
  dep_ranges = [(token_ids[1], token_ids[-1]+1) for _, token_ids in matches]

  # merge ranges
  refined_matches = merge(dep_ranges)
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
