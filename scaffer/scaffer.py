from __future__ import print_function
import os
import argp
import glob
import urllib

TEMPLATE_ROOT = "https://raw.githubusercontent.com/vivainio/scaffer-templates/master/templates/%s"
GITIGNORE = "https://raw.githubusercontent.com/github/gitignore/master/%s.gitignore"

def emit_file(pth, cont):
    print("- Emit", pth)
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


def main():
    argp.init()
    argp.sub("barrel", do_barrel)
    argp.sub("mit", do_mit)
    gi = argp.sub("gitignore", do_gitignore)
    gi.arg("--net", action="store_true")
    gi.arg("--python", action="store_true")
    argp.sub("setup", do_setuppy)
    argp.parse()

if __name__ == "__main__":
    main()