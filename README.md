# Scaffer

Create stuff like index.ts files (barrels), add mit license, setup.py, gitignore

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

# License

MIT.