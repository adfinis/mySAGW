"""Setuptools package definition."""

from setuptools import find_packages, setup

setup(
    name="mysagw",
    version="0.0.0",
    author="adfinis-sygroup",
    description="Application management for SAGW",
    url="https://github.com/adfinis-sygroup/mySAGW",
    license="License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    packages=find_packages(),
)
