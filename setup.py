from setuptools import setup

setup(
    name='WikiChatter',
    version='0.3.0',
    description='Parser for MediaWiki talk pages',
    url='https://github.com/kjschiroo/WikiChatter',

    author='Kevin Schiroo',
    author_email='kjschiroo@gmail.com',
    license='MIT',

    packages=['wikichatter'],
    install_requires=['mwparserfromhell']
)
