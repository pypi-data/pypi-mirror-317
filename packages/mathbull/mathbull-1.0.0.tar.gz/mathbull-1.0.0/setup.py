from setuptools import setup, find_packages

setup(
    name="mathbull",
    version="1.0.0",
    description="A full mathematical library for various calculations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="A.AB",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
