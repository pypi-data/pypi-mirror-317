import sys

VOCAB_LABELS = ["NOUN", "ADJ", "ADV", "PREP", "VERB", "PRON", "DETERMINER", "CONJ"]


NOUN_RULES = ["noun_proper", "noun_countability", "noun_with_indefinite_art", "noun_with_definite_art"]

ADJ_RULES = ["adj_ending_in_ed", "adj_ending_in_ing", "adj_order", "adj_for_equal_comparisons", "adj_comparative", "adj_superlative"]

ADV_RULES = ["adv_of_frequency", "adv_of_manner", "adv_of_time", "adv_of_place", "adv_of_degree", "adv_for_equal_comparisons", "adv_comparative", "adv_superlative"]

PREP_RULES = ["prep_with_verb", "prep_with_adj", "prep_with_noun"]

VERB_RULES = ["verb_passive_voice", "verb_simple_present_tense", "verb_simple_past_tense", "verb_simple_future_tense", "verb_present_progressive_tense", "verb_past_progressive_tense", "verb_present_perfect_tense", "verb_past_perfect_tense", "verb_copular", "verb_modal", "verb_transitive", "verb_intransitive"]

PRON_RULES = ["pron_personal", "pron_possessive", "pron_reflexive", "pron_relative", "pron_interrogative"]

DETERMINER_RULES = ["det_cardinal_num", "det_indefinite_art", "det_definite_art"]

CONJ_RULES = ["conj_subordinating", "conj_coordinating"]

SEN_LABELS = ["NOMINAL_CLAUSE", "RELATIVE_CLAUSE", "SUBJUNCTIVE_MOOD"]

NOMINAL_CLAUSE_RULES = ["nominal_subject_clause", "nominal_object_clause", "nominal_predicative_clause"]

RELATIVE_CLAUSE_RULES = ["relative_clause"]

SUBJUNCTIVE_MOOD_RULES = ["subjunctive_present", "subjunctive_past", "subjunctive_future"]

LABELS = VOCAB_LABELS + SEN_LABELS

LABEL_RULES = {label: getattr(sys.modules[__name__], label+"_RULES") for label in LABELS}


