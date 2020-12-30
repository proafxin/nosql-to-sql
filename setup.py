from setuptools import (
    setup,
    find_packages,
)

setup(
    name='nosql_to_sql',
    version='1.0',
    author_email='billalmasum93@gmail.com',
    url='https://github.com/proafxin/no-sql-to-sql',
    project_urls={
        #'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        #'Funding': 'https://donate.pypi.org',
        #'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/proafxin/no-sql-to-sql',
        #'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },
    description='This module converts denormalized NoSQL data to plain SQL data.',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pandas'],
    license='MIT',
)