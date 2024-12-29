from setuptools import setup, find_packages

setup(
    name="dataless",
    version="1.0",
    author="Azib Farooq",
    description="Library for Implementation of the dataless Neural Network for range of NP-hard problems",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
