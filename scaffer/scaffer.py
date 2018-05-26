from __future__ import print_function
import os
import argp
import glob
import urllib
import json
import pprint
import itertools
import emitter

TEMPLATE_ROOT = "https://raw.githubusercontent.com/vivainio/scaffer-templates/master/templates/%s"
GITIGNORE = "https://raw.githubusercontent.com/github/gitignore/master/%s.gitignore"

def ensure_dir_for(pth):
    dname = os.path.dirname(pth)
    if not os.path.isdir(dname):
        os.makedirs(dname)


def emit_file(pth, cont):
    print("- Emit", pth)
    ensure_dir_for(pth)
    if os.path.exists(pth):
        print("Can't overwrite", pth)
        return
    open(pth,"w").write(cont)

def fetch_url_to(fname, url):
    print("- Emit", fname, url)
    urllib.urlretrieve(url, fname)

def fetch_template_to(fname, urlpath):
    template_url = TEMPLATE_ROOT % urlpath
    fetch_url_to(fname, template_url)

def do_gitignore(args):
    if args.net:
        name = "VisualStudio"
    elif args.python:
        name = "Python"
    else:
        print("Must specify language! (--net, --python)")
        return

    fetch_url_to(".gitignore", GITIGNORE % name)


def do_barrel(arg):
    """ Create index.ts barrel in current directory """

    files = glob.glob("*.ts")
    lines = ['export * from "./%s";' % os.path.splitext(f)[0] for f in files ]

    emit_file("index.ts", "\n".join(lines))

def do_mit(arg):
    """ create MIT license in project """
    fetch_template_to("LICENSE", "MIT_LICENSE")

def do_setuppy(arg):
    """ Create setup.py """
    fetch_template_to("setup.py", "setup_py.py")


def discover_files_in_parents(filenames, startdir):
    cur = startdir
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
    files = discover_files_in_parents(['package.json', 'scaffer.json'], os.getcwd())
    for f in files:
        dirs = get_key_from_json(f, "scaffer")
        if not dirs:
            continue
        rdir = os.path.dirname(f)
        for d in dirs:
            templates = os.listdir(os.path.join(rdir,d))
            for t in templates:
                yield (t, os.path.join(rdir,d,t))

def do_gen(arg):
    """ Generate complex template """

    tgt_dir = os.getcwd()

    ts = find_templates()
    if not arg.template:
        pprint.pprint(list(ts))
        return
    to_gen = (t for t in ts if t[0] in arg.template)

    for template in to_gen:
        os.chdir(template[1])
        content = list(emitter.files_with_content("."))
        all_content = "".join(t[1] for t in content)

        vars = emitter.discover_variables(all_content)
        filled = emitter.fill_variables(vars)
        renderings = emitter.var_renderings(filled)
        new_cont = emitter.rendered_content(content, renderings)
        for fname, content in new_cont:
            absname = os.path.join(tgt_dir, fname)
            emit_file(absname, content)

def main():
    argp.init()
    argp.sub("barrel", do_barrel)
    argp.sub("mit", do_mit)
    gi = argp.sub("gitignore", do_gitignore)
    gi.arg("--net", action="store_true")
    gi.arg("--python", action="store_true")
    argp.sub("setup", do_setuppy)
    gen = argp.sub("gen", do_gen, help="Generate from complex template")
    gen.arg('-v', help="Give value to variable")
    gen.arg("template", help="Template to generate", nargs="?")
    argp.parse()

if __name__ == "__main__":
    main()