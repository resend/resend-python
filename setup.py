#!/usr/bin/env python

from setuptools import setup

install_requires = open("requirements.txt").readlines()

setup(
    name="klotty",
    version="0.0.1",
    description="Klotty Python SDK",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    author="Derich Pacheco",
    author_email="carlosderich@gmail.com",
    url="https://github.com/drish/klotty-py",
    packages=["klotty"],
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    python_requires=">3.7.5",
    keywords=["email", "email platform"],
    classifiers=[
        "Development Status :: 3 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
