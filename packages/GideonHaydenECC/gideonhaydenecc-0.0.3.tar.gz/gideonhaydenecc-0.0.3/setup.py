from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Elliptic curve python package'
LONG_DESCRIPTION = 'Python package that facilitates the arithmetic operations on elliptic curves both over reals and finite fields'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="GideonHaydenECC", 
        version=VERSION,
        author="Gideon Hayden",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy',
                          'scipy',
                          'matplotlib',
                          'sympy'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
