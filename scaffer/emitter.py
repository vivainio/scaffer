from __future__ import print_function

import os
import re
import itertools



def discover_variables(cont):
    locase_spans = re.findall(r"scf[\.\-\_]([a-z]+)", cont)
    upcase_spans = list((u.lower() for u in re.findall(r"Scf([A-Z][a-z]+)", cont)))
    return set(locase_spans + upcase_spans)


def get_renderings(var_name, var_value):
    parts = var_value.split("-")
    return [
        ("scf." + var_name, ".".join(parts)),
        ("scf-" + var_name, "-".join(parts)),
        ("scf_" + var_name, "_".join(parts)),
        ("Scf" + var_name.title(), "".join(p[0].upper() + p[1:] for p in parts))
    ]

def apply_replacements(content, replacements):
    cont = content
    for (fr,to) in replacements:
        cont = cont.replace(fr, to)
    return cont

def rendered_content(template, replacements):
    return [
        (apply_replacements(fname, replacements), apply_replacements(content, replacements)) for (fname, content) in template
    ]

def prompt_variables(vars):
    d = {}
    print("Will need variables:", ", ".join(vars))
    print("Use snake-case. E.g. if you want MyClass, enter 'my-class'.")
    for v in vars:
        val = raw_input("%s: " % v)
        d[v] = val.strip()
        print(get_renderings(v,val))
    return d

def var_renderings(d):
    return list(itertools.chain(*[get_renderings(k,v) for (k,v) in d.items()]))

def files_with_content(rootdir):
    """ -> (fname, content)[] """
    for dirpath, _, fnames in os.walk(rootdir):
        for f in fnames:
            dp = os.path.join(dirpath, f)
            yield (dp, open(dp).read())
