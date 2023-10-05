from scaffer import emitter, scaffer
import sys
import pprint
from pathlib import Path
import os

os.chdir(Path(__file__).absolute().parent)

def test_binary():
    assert emitter.is_binary_content(b"hello\0")
    assert not emitter.is_binary_content(b"hello\r\n")

def test_files_with_content():
    files = list(emitter.files_with_content("."))
    names = [t for (t, _) in files]
    assert b".%sscaffer.json" % (os.sep.encode()) in names
    for c in [cont for (_,cont) in files]:
        assert isinstance(c, bytes)

def test_get_template_list():
    found = list(scaffer.find_templates())
    pprint.pprint(found)
    templates = set(n for (n,_) in found)
    musthave = set(["s1", "s2"])
    assert musthave.issubset(templates)

def test_run_g_without_args():
    sys.argv = ["scaffertest", "g"]
    scaffer.main()

def test_run_generate_template():
    sys.argv = ["scaffertest", "g", "s2", "--dry"]
    scaffer.main()