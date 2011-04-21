import simplenlp
def test_preprocess():
    assert simplenlp.preprocess_text('This is a\000 test.\r\n') == 'This is a test. '
