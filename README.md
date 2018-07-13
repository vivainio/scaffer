# Scaffer

Yet another scaffolding tool. This is the one that actually does what you want, honest. If you are not a reading type of
person, [see demo on YouTube](https://www.youtube.com/watch?v=WrXONcpl87A).

Unlike many other scaffolding tools (like cookiecutter, angular schematics etc), this one:

- Allows using working/compiling code as templates. That is, you only need to rename symbols in your live code and
it will still compile and/or run. That way can modify and test templates naturally without having to remaster the template for publication.
- Does not require you to create any configuration for your templates. Just place the files somewhere and use.
- Allows using templates from your own repo/source tree.
- Allows tree to contain as many templates as you want. E.g. with cookiecutter, you are stuck with one template per repo.
- Is turing complete! You can add [scaffer_init.py](https://github.com/vivainio/scaffer-templates/blob/master/templates/cs-lib/scaffer_init.py) 
  to your template, e.g to read values to template variables from external system (say, call git to get username, 
  check directory name to get project name...)
- Is not implemented in Node.

## Logic

If you want to have template variable 'myvar', represent it by one of these in the templates:

ScfMyvar, scf-myvar, scf.myvar, scf_myvar, or uppercase equivalents.

Example of file with all the supported templates, targeting variables "prj" and "bar":
```
ScfPrjHello vs ScfBarWorld in pascalcase.
Lower kebab scf-prj-hello scf-bar-world
Lower snake scf_prj_hello scf_bar_world
Lower dotted scf.prj.hello scf.bar.world
Lower flat scfprj scfbar
Upper dotted SCF.PRJ.HELLO SCF.BAR.world
Upper kebab SCF-PRJ-HELLO SCF-BAR-world
Upper snake SCF_PRJ_HELLO SCF_BAR_world
Upper flat SCFPRJ SCFBAR
```

Note that the "flat" variants (`scfprj` or `SCFPRJ`) can't contain a suffix for obvious reasons.

When scaffer sees these markers in your templates, it will ask for these and do a smart search-and-replace operation that does
PascalCasing, kebab-casing, dot.separation and snake_casing based on what notation you used in the template.

The user will always give a kebab-cased variation when prompted. So if the user wants to emit MyClass, she just enters
my-class when prompted. Scaffer will know how to emit the right compound word format at the replacement sites.

Template variables can also be in file and directory names, and behave as you would expect.

See https://github.com/vivainio/scaffer-templates for example templates.

## Template discovery

1. Place your files somewhere.
2. In project root, or any parent directory, put scaffer.json that points to directories that contain your templates:

```json

{
    "scaffer": ["my/templates", "some/other/templates"]
}

```


You can also put that "scaffer" key in your package.json if you don't want to pollute your tree with new files.


# Installation

```
pip install scaffer
```

Usage:

```
usage: scaffer [-h] {barrel,gitignore,setup,g,add} ...

positional arguments:
  {barrel,gitignore,setup,g,add}
    barrel              Create index.tx for current directory
    gitignore           Create .gitignore file
    g                   Generate code from named template
    add                 Add current directory as template root in user global
                        scaffer.json

$ scaffer g -h

usage:  g [-h] [-v variable=value [variable=value ...]] [-f] [template]

positional arguments:
  template              Template to generate

optional arguments:
  -h, --help            show this help message and exit
  -v variable=value [variable=value ...]
                        Give value to variable
  -f                    Overwrite files if needed

```


# License

MIT.
