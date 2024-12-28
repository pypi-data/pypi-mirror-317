# coding='utf-8'

from setuptools import setup
long_description = open('README.md').read()
setup(
    name='myhttps',
    version='0.0.11',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Yang Li',
    author_email='leeyang1991@gmail.com',
    packages=['myhttps'],
    url='https://github.com/leeyang1991/myhttps',
    python_requires='>=3',
    install_requires=[
    'pyOpenSSL',
    'outdated',
    ],
)
