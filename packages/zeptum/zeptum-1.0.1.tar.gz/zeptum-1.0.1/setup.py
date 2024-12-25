from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zeptum",
    version="1.0.1",
    description="database package, simple and lightweight, without encryption, not recommended for use on servers with public access.",
    author="harttman",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
