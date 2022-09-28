#!/usr/bin/env python


import pathlib
import setuptools


requires = [
    # nothing thus far ;)
]

root = pathlib.Path(__file__).parent.resolve()
with (root / 'README.md').open('r', encoding='utf-8') as f:
    readme = f.read()

about = {}
with (root / 'cogpyt' / '__about__.py').open('r', encoding='utf-8') as f:
    exec(f.read(), about)

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    author=about['__author__'],
    long_description=readme,
    license=about['__licence__'],
    long_description_content_type='text/markdown',
    url=about['__url__'],
    packages=setuptools.find_packages(),
    package_data={'': ['LICENSE']},
    package_dir={'cogpyt': 'cogpyt'},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=requires,
)
