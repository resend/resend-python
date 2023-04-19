#!/usr/bin/env python

from setuptools import setup

from resend.version import get_version

install_requires = open("requirements.txt").readlines()

setup(
    name="resend",
    version=get_version(),
    description="Resend Python SDK",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    author="Derich Pacheco",
    author_email="carlosderich@gmail.com",
    url="https://github.com/drish/resend-py",
    packages=["resend"],
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    python_requires=">=3.7",
    keywords=["email", "email platform"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
