"""Standardized closed-class English function words for stylometric analysis."""

PREPOSITIONS: frozenset[str] = frozenset({
    "about", "above", "across", "after", "against", "along", "among", "around",
    "at", "before", "behind", "below", "beneath", "beside", "between", "beyond",
    "by", "down", "during", "except", "for", "from", "in", "inside", "into",
    "like", "near", "of", "off", "on", "onto", "out", "outside", "over", "past",
    "since", "through", "throughout", "to", "toward", "under", "underneath",
    "until", "up", "upon", "with", "within", "without",
})

PRONOUNS: frozenset[str] = frozenset({
    "i", "me", "my", "mine", "myself",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself",
    "she", "her", "hers", "herself",
    "it", "its", "itself",
    "we", "us", "our", "ours", "ourselves",
    "they", "them", "their", "theirs", "themselves",
    "this", "that", "these", "those",
    "who", "whom", "whose", "which", "what",
    "anyone", "anybody", "anything",
    "everyone", "everybody", "everything",
    "someone", "somebody", "something",
    "nobody", "nothing",
})

CONJUNCTIONS: frozenset[str] = frozenset({
    "and", "but", "or", "nor", "for", "yet", "so",
    "although", "because", "since", "unless", "while",
    "where", "if", "than", "whether", "as", "though",
    "whereas", "whenever", "wherever",
})

AUXILIARY_VERBS: frozenset[str] = frozenset({
    "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having",
    "do", "does", "did",
    "can", "could", "will", "would", "shall", "should",
    "may", "might", "must",
})

DETERMINERS: frozenset[str] = frozenset({
    "the", "a", "an", "each", "every", "all", "both",
    "few", "some", "any", "no", "either", "neither",
    "much", "many", "several",
})

ALL_FUNCTION_WORDS: frozenset[str] = (
    PREPOSITIONS | PRONOUNS | CONJUNCTIONS | AUXILIARY_VERBS | DETERMINERS
)
