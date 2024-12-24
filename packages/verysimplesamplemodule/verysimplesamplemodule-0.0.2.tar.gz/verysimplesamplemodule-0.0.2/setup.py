from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A simple package to understand how to create a package'
LONG_DESCRIPTION = 'A package that allows to understand how to create a package'

# Setting up
setup(
    name="verysimplesamplemodule",
    version=VERSION,
    author="Myself",
    author_email="<email@email.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[], # add any additional packages that

    keywords=['python', 'package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)