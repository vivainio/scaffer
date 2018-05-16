# Scaffer

Create stuff like index.ts files (barrels), add mit license, setup.py, gitignore.

Unlike many other scaffolding tools, this one:

- Is not implemented in Node
- Creates files in your current directory, not "new project under separate directory".
- Has nontrivial commands. E.g. "scaffer barrel" command adds index.ts with export-throughs for all .ts files in current directory.

It's the missing "dotnet new gitignore"!

# Insallation

```
pip install scaffer
```

Usage:

```
usage: scaffer-script.py [-h] {barrel,mit,gitignore,setup} ...

positional arguments:
  {barrel,mit,gitignore,setup}

optional arguments:
  -h, --help            show this help message and exit


λ  scaffer gitignore
Must specify language! (--net, --python)
λ  scaffer gitignore --net
- Emit .gitignore https://raw.githubusercontent.com/github/gitignore/master/VisualStudio.gitignore

```

Future plans: discover and emit cookiecutter templates, do usual repetitive stuff.

The templates used are in https://github.com/vivainio/scaffer-templates

# License

MIT.
