from simplenlp.euro import LemmatizedEuroNL

# FIXME: this global is a temporary hack.
EXTRA_STOPWORDS = ['also', 'not', 'without', 'ever', 'because', 'then', 'than', 'do', 'just', 'how', 'out', 'much', 'both', 'other']

class SimpleNegationNL(LemmatizedEuroNL):
    """
    A NL processor where it's reasonable to negate anything between
    certain words and punctuation.
    """
    def __init__(self, lang, negation, punctuation, **kwargs):
        self.negation = negation
        self.punctuation = punctuation
        super(SimpleNegationNL, self).__init__(lang, **kwargs)

    def extract_concepts_with_negation(self, text, **kwargs):
        if isinstance(text, basestring):
            words = self.tokenize(text).split()
        else:
            words = text
        # FIXME: this may join together words from different contexts...
        positive_words = []
        negative_words = []
        neg_tagged_words = []
        pos_tagged_words = []
        positive = True
        for word in words:
            if word.startswith('#-'):
                neg_tagged_words.append('#'+word[2:])
            elif word.startswith('#'):
                pos_tagged_words.append(word)
            elif word.lower() in self.negation:
                positive = False
            elif word in EXTRA_STOPWORDS:
                continue
            else:
                if positive:
                    positive_words.append(word)
                else:
                    negative_words.append(word)
                if word in self.punctuation:
                    positive = True
        positive_concepts = [(c, 1) for c in self.extract_concepts(' '.join(positive_words), **kwargs)]
        negative_concepts = [(c, -1) for c in self.extract_concepts(' '.join(negative_words), **kwargs)]
        neg_tagged_concepts = [(c, -1) for c in neg_tagged_words]
        pos_tagged_concepts = [(c, 1) for c in pos_tagged_words]
        return positive_concepts + pos_tagged_concepts + negative_concepts + neg_tagged_concepts


negation = ['no', 'not', 'never', 'stop', 'lack', "n't", "without"]
punctuation = ['.', ',', '!', '?', '...', '-', ':', ';', '``', "''", "`", "'"]

exceptions = {
    u'people': (u'person', u's'),
    u'ground': (u'ground', u''),
}

def NL():
    return SimpleNegationNL('en', exceptions=exceptions,
                            negation=negation, punctuation=punctuation)

def test_negation_and_lemmatizing():
    from nose.tools import eq_
    doc = 'positives not #positives negatives #-negatives'
    nl = NL()
    concepts = nl.extract_concepts_with_negation(doc)
    eq_(sorted(concepts), sorted([('positive', 1),
                                  ('#positives', 1),
                                  ('negative', -1),
                                  ('#negatives', -1)]))
    
