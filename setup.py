from setuptools import setup

setup(
    name='pcfg_parser',
    version='0.1',
    description='PCFG Parser',
    author='Johannes Gontrum',
    author_email='gontrum@me.com',
    include_package_data=True,
    license='MIT license',
    entry_points={
          'console_scripts': [
              'treebank_to_cnf = pcfg_parser.scripts.treebank_to_cnf:main',
              'treebank_to_grammar = pcfg_parser.scripts.treebank_to_grammar:main',
              'parse = pcfg_parser.scripts.parse:main',
              'evaluate = pcfg_parser.scripts.evaluate:main'

          ]
      }
)
