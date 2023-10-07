from scaffer import emitter, scaffer
import sys
import pprint
from pathlib import Path
import os
import io
import zipfile

os.chdir(Path(__file__).absolute().parent)


def test_binary():
    assert emitter.is_binary_content(b"hello\0")
    assert not emitter.is_binary_content(b"hello\r\n")


def test_files_with_content():
    files = list(emitter.files_with_content("."))
    names = [t for (t, _) in files]
    assert b"./scaffer.json".replace(b"/", os.sep.encode()) in names
    assert b"./excluded_dir/dummy.txt".replace(b"/", os.sep.encode()) not in names
    assert b"./dummy.excluded".replace(b"/", os.sep.encode()) not in names
    for c in [cont for (_, cont) in files]:
        assert isinstance(c, bytes)


def test_get_template_list():
    found = list(scaffer.find_templates())
    pprint.pprint(found)
    templates = set(n for (n, _) in found)
    musthave = set(["s1", "s2", "url1", "url2"])
    assert musthave.issubset(templates)


def test_run_g_without_args():
    sys.argv = ["scaffertest", "g"]
    scaffer.main()


def test_run_generate_template():
    sys.argv = ["scaffertest", "g", "s2", "--dry"]
    scaffer.main()


def test_run_generate_named_template_http(requests_mock):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("dummy.txt", "dummy")
    requests_mock.get("http://localhost/1", content=zip_buffer.getvalue())
    sys.argv = ["scaffertest", "g", "url1", "--dry"]
    scaffer.main()


def test_run_generate_template_http(requests_mock, fs):  # Requires pyfakefs fixture
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("dummy2.txt", "dummy")
        zf.writestr("dummy2.excluded", "dummy")
        zf.writestr(".gitignore", "dummy2.excluded")
    requests_mock.get("http://localhost/1", content=zip_buffer.getvalue())
    sys.argv = ["scaffertest", "g", "http://localhost/1"]
    scaffer.main()
    assert os.path.exists("dummy2.txt")
    assert not os.path.exists("dummy2.excluded")
