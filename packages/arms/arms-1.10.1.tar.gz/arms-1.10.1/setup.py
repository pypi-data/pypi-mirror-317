# coding: utf-8
"""
arms
~~~~~~~~
CI/CD tool of Chongqing Parsec Corp.
Setup
-----
.. code-block:: bash
    > pip install arms
    > arms -h

"""

import ast
import re
from codecs import open  # To use a consistent encoding
from os import path

from setuptools import (  # Always prefer setuptools over distutils
    find_packages, setup)
from setuptools.command.install import install

_version_re = re.compile(r'__version__\s+=\s+(.*)')
version = str(ast.literal_eval(
    _version_re.search(
        open('arms/__init__.py').read()
    ).group(1)
))
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class MyInstall(install):
    def run(self):
        print("-- installing... --")
        install.run(self)


setup(
    name='arms',
    version=version,
    description='CI/CD tool of Chongqing Parsec Corp.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # 指定内容类型为Markdown
    url='https://pypi.python.org/pypi/arms',
    author='qorzj',
    author_email='inull@qq.com',
    license='MIT',
    platforms=['any'],
    classifiers=[
        # 在这里添加分类器
    ],
    keywords='arms armstrong chongqing',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'lesscli>=0.2.0',
        'rich',
        'pyperclip',
        'InquirerPy',
        'json5',
        'requests',
    ],
    cmdclass={'install': MyInstall},
    entry_points={
        'console_scripts': [
            'arms = arms.main:main'
        ],
    },
)
