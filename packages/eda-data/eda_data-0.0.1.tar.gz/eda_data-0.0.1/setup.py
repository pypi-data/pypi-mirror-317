from setuptools import find_packages, setup
from os import path
working_directrory = path.abspath(path.dirname(__file__))

with open(path.join(working_directrory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="eda-data",
    version="0.0.1",
    description="EDA Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="Gaurav Tyagi",
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "tqdm"
    ]
)