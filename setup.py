from setuptools import (
    setup,
    find_packages,
)

setup(
    name='flatten',
    version='1.1',
    author_email='billalmasum93@gmail.com',
    url='https://github.com/proafxin/nosql-to-sql',
    description='This module converts NoSQL data to plain SQL data.',
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