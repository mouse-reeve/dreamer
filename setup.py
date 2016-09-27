''' setup script '''
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Dreamer',
    version='0.0.1',

    description='generate dreams',
    long_description=long_description,

    url='https://github.com/mouse-reeve/dreamer',

    author='Mouse Reeve',
    author_email='mousereeve@riseup.net',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Artistic Software',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='generative dreams sleep',

    packages=['dreamer'],
    include_package_data=True,

    install_requires=['Tracery']
)
