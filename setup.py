from setuptools import setup
import proclib


setup(
    name='proclib',
    version=proclib.__version__,

    description='pythonic processes',
    long_description=open('README.rst').read(),
    license='MIT',

    author='Eeo Jun',
    author_email='packwolf58@gmail.com',
    url='https://github.com/datalib/proclib',

    packages=[
        'proclib',
        'proclib.tests',
        ],
    install_requires=[],
    extras_require={
        'test': ['pytest'],
    },

    include_package_data=True,
    zip_safe=False,

    keywords='processes unix process datalib',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        ],
    )
