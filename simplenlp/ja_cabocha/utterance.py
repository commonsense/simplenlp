from simplenlp.ja_cabocha.debug import *
from simplenlp.ja_cabocha.util  import *
from simplenlp.ja_cabocha.tree  import *

import MeCab
import CaboCha
import re

class JaUtterance(JaTreeBranch, JaLanguageNode):
    ''' Represents an entire utterance '''

    def __init__(self, children):
        JaTreeBranch.__init__(self)
        self.children  = children

        for child in self.children:
            child.parent = self

    dump_lines = JaDebug.dump_lines_utterance

    def __str__(self):
        return self.surface

    @shared_property
    def is_utterance(self):
        return True

from simplenlp.ja_cabocha.chunk  import *
from simplenlp.ja_cabocha.cabocha_token  import *
from simplenlp.ja_cabocha.parser import *

