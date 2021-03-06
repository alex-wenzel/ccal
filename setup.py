from setuptools import find_packages, setup

from ccal import VERSION

name = "ccal"

setup(
    name=name,
    version=VERSION,
    url="https://github.com/KwatME/{}".format(name),
    author="Kwat Medetgul-Ernar",
    author_email="kwatme8@gmail.com",
    packages=find_packages(),
    python_requires=">=3.6",
    package_data={"ccal": ["data"]},
)
