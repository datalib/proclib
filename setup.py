from setuptools import setup
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='proclib',
    version='0.0.1',

    description='pythonic processes',
    long_description=long_description,

    url='https://github.com/datalib/proclib',
    author='Eeo Jun',
    author_email='packwolf58@gmail.com',

    packages=['proclib'],
    install_requires=[],
    extras_require={
        'test': ['pytest'],
    },

    include_package_data=True,
    zip_safe=False,

    license='MIT',
    keywords='processes unix process datalib',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        ],
    )
