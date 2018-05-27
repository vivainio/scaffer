# Scaffer

The underengineered scaffolding tool.

Unlike many other scaffolding tools, this one:

- Allows using working/compiling code as templates. That is, you only need to rename symbols in your live code and
it will still compile and/or run.
- Does not require you to create any configuration for your templates. Just place the files somewhere and use.
- Allows using templates from your own repo/source tree
- Allows tree to contain as many templates as you want
- Is not implemented in Node

It's the missing "dotnet new gitignore"!

## Logic

If you want to have template variable 'myvar', represent in by one of these in the templates:

ScfMyvar, scf-myvar, scf.myvar, scf_myvar.

When scaffer sees these markers in your templates, it will ask for these and do a smart search-and-replace operation that does PascalCasing, kebab-casing, dot.separation and snake_casing based on what notation you used in the template.

The user will always give a snake-cased variation when prompted. So if the user wants to emit MyClass, she just enters
my-class when prompted. Scaffer will know how to emit the right word separation format at the replacement sites.

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


positional arguments:
  {barrel,mit,gitignore,setup}

optional arguments:
  -h, --help            show this help message and exit


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
