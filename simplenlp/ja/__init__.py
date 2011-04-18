# -*- coding: utf-8 -*-
from csc.nl import DefaultNL, preprocess_text
import subprocess

# MeCab outputs the part of speech of its terms. We can simply identify
# particular (coarse or fine) parts of speech as containing stopwords.

STOPWORD_CATEGORIES = set([
    u'助詞',          # coarse: particle
    u'連体詞',        # coarse: adnominal adjective ("rentaishi")
    u'助動詞',        # coarse: auxiliary verb
    u'接続詞',        # coarse: conjunction
    u'フィラー',      # coarse: filler
    u'記号',          # coarse: symbol
    u'助詞類接続',    # fine: particle connection
    u'代名詞',        # fine: pronoun
    u'接尾',          # fine: suffix
])

# Forms of particular verbs are also stopwords.
#
# A thought: Should the rare kanji version of suru not be a stopword?
# I'll need to ask someone who knows more Japanese, but it may be
# that if they're using the kanji it's for particular emphasis.
STOPWORD_VERBS = set([
    u'する',          # suru: to do
    u'為る',          # suru in kanji (very rare)
    u'くる',          # kuru: to come
    u'来る',          # kuru in kanji
    u'いく',          # iku: to go
    u'行く',          # iku in kanji
])

class MeCabNL(DefaultNL):
    """
    Handle Japanese text using the command-line version of MeCab.
    (mecab-python is convenient, but its installer is too flaky to rely on.)

    ja_cabocha gives more sophisticated results, but requires a large number of
    additional dependencies. Using this tool for Japanese requires only
    MeCab to be installed and accepting UTF-8 text.
    """
    def __init__(self):
        """
        Create a MeCabNL object by opening a pipe to the mecab command.
        """
        self.mecab = subprocess.Popen(['mecab'], shell=True, bufsize=1, close_fds=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    
    def __del__(self):
        """
        Clean up by closing the pipe.
        """
        self.mecab.stdin.close()
        del self.mecab
    
    def analyze(self, text):
        """
        Runs a line of text through MeCab, and returns the results as a
        list of lists.
        """
        text = preprocess_text(text).encode('utf-8')
        self.mecab.stdin.write(text+'\n')
        results = []
        out_line = ''
        while True:
            out_line = self.mecab.stdout.readline()
            if out_line == 'EOS\n':
                break
            word, info = out_line.strip('\n').split('\t')
            record = [word] + info.split(',')
            unicode_record = [entry.decode('utf-8') for entry in record]
            results.append(unicode_record)
        return results

    def tokenize_list(self, text):
        """
        Split a text into separate words.
        
        This does not de-agglutinate as much as ja_cabocha does, but the words
        where they differ are likely to be stopwords anyway.
        """
        return [record[0] for record in self.analyze(text)]

    def tokenize(self, text):
        """
        Split a text into words separated by spaces (due to our overly
        Eurocentric design decision).
        """
        return u' '.join(self.tokenize_list(text))
    
    def _is_stopword_record(self, record):
        """
        Determine whether a single MeCab record represents a stopword.
        """
        return (record[1] in STOPWORD_CATEGORIES or
                record[2] in STOPWORD_CATEGORIES or
                record[7] in STOPWORD_VERBS)

    def is_stopword(self, text):
        """
        Determine whether a single word is a stopword, or whether a short
        phrase is made entirely of stopwords, disregarding context.

        Use of this function should be avoided; it's better to give the text
        in context and let MeCab determine which words are the stopwords.
        """
        found_content_word = False
        for record in self.analyze(text):
            if not self._is_stopword_record(record):
                found_content_word = True
                break
        return not found_content_word

    def normalize_list(self, text):
        """
        Get a canonical list representation of Japanese text, with words
        separated and reduced to their base forms.
        """
        words = []
        analysis = self.analyze(text)
        for record in analysis:
            if not self._is_stopword_record(record):
                words.append(record[0])
        if not words:
            # Don't discard stopwords if that's all you've got
            words = [record[0] for record in analysis]
        return words

    def normalize(self, text):
        """
        Get a canonical string representation of Japanese text, like
        :meth:`normalize_list` but joined with spaces.
        """
        return ' '.join(self.normalize_list(text))

def NL():
    return MeCabNL()

