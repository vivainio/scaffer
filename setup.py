from distutils.core import setup

setup(name='Scaffer',
      version='0.3.0',
      description='Scaffold stuff',
      author='Ville M. Vainio',
      author_email='vivainio@gmail.com',
      url='https://github.com/vivainio/scaffer',
      packages=['scaffer'],
      install_requires=['argp'],
      entry_points = {
        'console_scripts': [
            'scaffer = scaffer.scaffer:main'
        ]
      }
     )
