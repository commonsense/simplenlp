# -*- coding: utf-8 -*-
import simplenlp
def test_chinese():
    zh = simplenlp.get('zh-Hant')
    railway = u"迪士尼线"
    assert zh.normalize(railway) == railway
