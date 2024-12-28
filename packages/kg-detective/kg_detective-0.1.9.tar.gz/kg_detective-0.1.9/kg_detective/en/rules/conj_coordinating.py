from spacy.matcher import Matcher, PhraseMatcher, DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for phrases with coordinating conjunctions 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  dep_matcher = DependencyMatcher(nlp.vocab)

  dep_patterns = [
    [
      {
        "RIGHT_ID": "conj",
        "RIGHT_ATTRS": {"POS": "CCONJ", "DEP": "cc"}
      },
      {
        "LEFT_ID": "conj",
        "REL_OP": "<",
        "RIGHT_ID": "A",
        "RIGHT_ATTRS": {}
      },
      {
        "LEFT_ID": "A",
        "REL_OP": ">",
        "RIGHT_ID": "B",
        "RIGHT_ATTRS": {"DEP": "conj"}
      }
    ],
  ]

  dep_matcher.add("conj_coodinating", dep_patterns)
  matches = dep_matcher(doc)

  for _, (conj, A, B) in matches:
    A_children = [cs.i for cs in doc[A].rights if cs.dep_!="conj" and cs.dep_!="cc" and cs.pos_!="PUNCT"] + [cs.i for cs in doc[A].lefts if cs.dep_=="preconj"]
    B_children = [cs.i for cs in doc[B].rights]

    A_children.append(A)
    B_children.append(B)
    #print(A_children)
    #print(B_children)
    
    A_tree_range = (min(A_children), max(A_children)+1)
    B_tree_range = (min(B_children), max(B_children)+1)

    s = 0
    if s < A_tree_range[0]:
      result.append({"text": doc[s:A_tree_range[0]].text, "highlight": False})
    result.append({"text": doc[A_tree_range[0]:A_tree_range[1]].text, "highlight": True, "meta": "pre"})
    s = A_tree_range[1]
    if s < conj:
      result.append({"text": doc[s:conj].text, "highlight": False})
    result.append({"text": doc[conj].text, "highlight": True, "meta": "conj"}) 
    s = conj+1
    if s < B_tree_range[0]:
      result.append({"text": doc[s:B_tree_range[0]].text, "highlight": False})
    result.append({"text": doc[B_tree_range[0]:B_tree_range[1]].text, "highlight": True, "meta": "post"})
  return result
