from setuptools import setup

VERSION = '0.0.8' 
DESCRIPTION = 'Ripoff Numpy'
LONG_DESCRIPTION = 'A library for manipulating matrices while boiling your RAM'

# Setting up
setup(
        name="Ramtrix", 
        version=VERSION,
        author="Ram",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,

        keywords=['python', 'matrices', 'row reduction', 'linear algebra'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)