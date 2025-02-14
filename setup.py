from setuptools import setup, find_packages

setup(
    name="datacrunch_api",
    version="0.1.0",
    author="Knut Hellan",
    author_email="knut@findable.ai",
    description="Datacrunch API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/findable-no/datacrunch_api",
    packages=find_packages(),
    install_requires=[
        "requests",
        "typer",
        "rich",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
)
