# -*- coding: utf-8 -*-
import simplenlp

def test_normalize():
    ja = simplenlp.get('ja')
    test_sentence = u'これはテストですが、大丈夫です。'
    assert ja.normalize_list(test_sentence) == [u'テスト', u'大丈夫']
    assert ja.normalize(test_sentence) == u'テスト 大丈夫'

def test_nai():
    ja = simplenlp.get('ja')
    test_sentence = u'いいえ、分かりませんでした。'
    assert ja.normalize(test_sentence) == u'いいえ 分かる ない'

