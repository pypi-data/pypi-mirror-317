from setuptools import setup, find_packages

setup(
    name="amrita-converter",
    version="0.1.0",
    author="Amrita",
    author_email="amrandal09@gmail.com",
    description="A simple function that can calculate the series and factorial of a number ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amrita09-pix/converter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
