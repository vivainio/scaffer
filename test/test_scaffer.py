from scaffer import emitter

def test_binary():
    assert emitter.is_binary_content(b"hello\0")
    assert not emitter.is_binary_content(b"hello\r\n")

def test_files_with_content():
    files = list(emitter.files_with_content("."))
    names = [t for (t, _) in files]
    assert b".\\scaffer.json" in names
    for c in [cont for (_,cont) in files]:
        assert isinstance(c, bytes)
