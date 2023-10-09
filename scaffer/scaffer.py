import os
import argp
import json
from . import emitter
import functools
from contextlib import contextmanager
import tempfile
import zipfile
import io

import requests

RC_FILE = os.path.expanduser("~/.scaffer/scaffer.json")


def ensure_dir_for(pth):
    dname = os.path.dirname(pth)
    if dname and not os.path.isdir(dname):
        os.makedirs(dname)


def emit_file(pth: bytes, cont, overwrite=False, dry=False):
    if dry:
        print(f"- Would emit {pth.decode()} [{len(cont)}]")
        return
    print(f"- Emit {pth.decode()}")

    ensure_dir_for(pth)
    if os.path.exists(pth) and not overwrite:
        print("Can't overwrite '%s', use -f to force" % pth.decode())
        return
    open(pth, "wb").write(cont)


def discover_files_in_parents(filenames, start_dir):
    cur = start_dir
    while 1:
        for fname in os.listdir(cur):
            if fname in filenames:
                fpath = os.path.join(cur, fname)
                yield fpath
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent


def get_key_from_json(fname, key):
    try:
        c = json.load(open(fname))
    except ValueError:
        return None
    return c.get(key)


def find_templates():
    files = list(
        discover_files_in_parents(["package.json", "scaffer.json"], os.getcwd())
    )
    home_rc = os.path.expanduser("~/.scaffer/scaffer.json")
    if os.path.isfile(home_rc):
        files.append(home_rc)

    for f in files:
        dirs = get_key_from_json(f, "scaffer")
        if not dirs:
            continue
        rdir = os.path.dirname(f)
        for d in dirs:
            tdir = os.path.join(rdir, d)
            if not os.path.isdir(tdir):
                print("Warning! Missing:", tdir)
                continue

            templates = os.listdir(tdir)
            for t in templates:
                full = os.path.normpath(os.path.join(tdir, t))
                if os.path.isdir(full):
                    yield t, full
        urls = get_key_from_json(f, "scaffer_template_urls") or {}
        for t, url in urls.items():
            yield t, url


def longest_string(seq):
    return functools.reduce(lambda current, s: max(current, len(s)), seq, 0)


@contextmanager
def _target_dir(target):
    if target.startswith("http://") or target.startswith("https://"):
        print("Downloading template from:", target)
        with tempfile.TemporaryDirectory() as temp_dir_name:
            print("Temp directory:", temp_dir_name)
            response = requests.get(target)
            response.raise_for_status()
            z = zipfile.ZipFile(io.BytesIO(response.content))
            z.extractall(temp_dir_name)
            yield temp_dir_name
    else:
        yield target


def do_gen(arg):
    """Generate complex template"""
    tgt_dir = os.getcwd().encode()
    ts = sorted(find_templates())
    if not arg.template:
        print("No template specified. Available templates:")
        maxlen = longest_string(t[0] for t in ts)
        for n, p in ts:
            print("%s%s" % (n.ljust(maxlen + 2, " "), p))
        return
    if arg.template.startswith("http://") or arg.template.startswith("https://"):
        to_gen = [(None, arg.template)]
    elif os.path.isdir(arg.template):
        to_gen = [(arg.template, arg.template)]
    else:
        to_gen = [t for t in ts if t[0] == arg.template]
    if not to_gen:
        print("ERROR: Template not found:", arg.template)
        return

    for _, target in to_gen:
        with _target_dir(target) as target_dir:
            old_dir = os.getcwd()
            os.chdir(target_dir)
            content = list(emitter.files_with_content("."))
            all_content = b"".join(
                t[0] + b"\n" + (b"" if emitter.is_binary_content(t[1]) else t[1])
                for t in content
            )
            os.chdir(old_dir)
            prefilled_vars = {
                k.encode(): v.encode() for (k, v) in (a.split("=", 1) for a in arg.v)
            }
            variables = emitter.discover_variables(all_content)
            if os.path.isfile("scaffer_init.py"):
                emitter.run_scaffer_init(
                    os.path.abspath("scaffer_init.py"),
                    variables,
                    prefilled_vars,
                    tgt_dir,
                )

            unknown_prefilled = set(prefilled_vars.keys()).difference(variables)
            if unknown_prefilled:
                print(
                    "Warning! Unknown variables on command line:",
                    b", ".join(unknown_prefilled),
                )
            to_fill = variables.difference(set(prefilled_vars.keys()))
            filled = emitter.prompt_variables(to_fill) if to_fill else {}
            filled.update(prefilled_vars)
            renderings = emitter.var_renderings(filled)
            new_cont = emitter.rendered_content(content, renderings)

            for fname, content in new_cont:
                absname = os.path.normpath(os.path.join(tgt_dir, fname))
                emit_file(absname, content, arg.f, arg.dry)


def read_rc():
    if not os.path.isfile(RC_FILE):
        return {}
    return json.load(open(RC_FILE))


def write_rc(d):
    ensure_dir_for(RC_FILE)
    json.dump(d, open(RC_FILE, "w"), indent=2)


def do_add(arg):
    """Add current directory to global templates directory"""
    old = read_rc()
    olddirs = old.get("scaffer", [])
    olddirs.append(os.getcwd())
    old["scaffer"] = sorted(set(olddirs))
    write_rc(old)


def main():
    argp.init()

    # g
    gen = argp.sub("g", do_gen, help="Generate code from named template")
    gen.arg(
        "-v",
        help="Give value to variable",
        nargs="+",
        default=[],
        metavar="variable=value",
    )
    gen.arg("-f", help="Overwrite files if needed", action="store_true")
    gen.arg("--dry", action="store_true", help="Dry run, do not create files")
    gen.arg("template", help="Template to generate", nargs="?")

    argp.sub(
        "add",
        do_add,
        help="Add current directory as template root in user global scaffer.json",
    )
    argp.parse()


if __name__ == "__main__":
    main()
