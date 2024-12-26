from setuptools import setup, find_packages

setup(
    name="seros",  # Package name
    version="0.1.0",  # Version number
    author="Thirupathi",
    author_email="suryathirupks@gmail.com",
    description="A Python module for finding prime numbers using the Sieve of Eratosthenes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
