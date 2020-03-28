from scaffer import emitter, scaffer
import sys

def test_binary():
    assert emitter.is_binary_content(b"hello\0")
    assert not emitter.is_binary_content(b"hello\r\n")

def test_files_with_content():
    files = list(emitter.files_with_content("."))
    names = [t for (t, _) in files]
    assert b".\\scaffer.json" in names
    for c in [cont for (_,cont) in files]:
        assert isinstance(c, bytes)

def test_get_template_list():
    templates = set(n for (n,_) in scaffer.find_templates())
    musthave = set(["s1", "s2"])
    assert musthave.issubset(templates)

def test_run_g_without_args():
    sys.argv = ["scaffertest", "g"]
    scaffer.main()

def test_run_generate_template():
    sys.argv = ["scaffertest", "g", "s2", "--dry"]
    scaffer.main()