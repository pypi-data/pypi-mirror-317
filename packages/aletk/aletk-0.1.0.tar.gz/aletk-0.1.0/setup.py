from setuptools import setup, find_packages

setup(
    name = "aletk",
    version = "0.1.0",
    packages = find_packages(
        exclude = [
            'prototypes',
            'tests',
        ]
    ),
    install_requires = [
        'fuzzywuzzy',
        'python-Levenshtein',  # to improve performance of fuzzywuzzy
    ],
    extras_require={
        'dev': [
            'mypy',       # for static type checking
            'black',      # for code formatting
            'pytest',     # for testing
            'jupyter',    # for prototyping in notebooks
        ],
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.13',
)
