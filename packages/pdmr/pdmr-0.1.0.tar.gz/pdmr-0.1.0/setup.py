# setup.py
from setuptools import setup, find_packages

setup(
    name="pdmr",  # Changed to pdmr
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "tqdm>=4.60.0",
    ],
    author="Toan Doan",
    author_email="toandoan261120@gmail.com",
    description="pdmr: Pandas Multiprocess Runner - A library for running functions on Pandas DataFrames with multiprocessing and checkpointing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/t3bol90/pdmr",  # Update with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)