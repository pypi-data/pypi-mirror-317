from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pykugram",
    version="0.1.1",
    description="Package under development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CortextDEV",
    packages=find_packages(),
    python_requires='>=3.11.9',
)