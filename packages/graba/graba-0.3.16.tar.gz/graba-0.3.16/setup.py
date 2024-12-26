from setuptools import setup, find_packages

setup(
    name="graba",
    version="0.3.16",
    description="A library to generate random value for different concepts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Francisco Jose Albert Albusac",
    author_email="francis.jaa@protonmail.com",
    url="https://github.com/tatitati/graba",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)