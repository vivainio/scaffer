from setuptools import setup

setup(
    name="Scaffer",
    version="1.3.0",
    description="Scaffolding tool (code template emitter)",
    author="Ville M. Vainio",
    author_email="vivainio@gmail.com",
    url="https://github.com/vivainio/scaffer",
    packages=["scaffer"],
    install_requires=["argp", "gitignore-parser", "requests"],
    entry_points={"console_scripts": ["scaffer = scaffer.scaffer:main"]},
)
