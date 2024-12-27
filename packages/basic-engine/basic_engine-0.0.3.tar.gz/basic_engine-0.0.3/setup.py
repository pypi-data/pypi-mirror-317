from setuptools import setup, find_packages
from src.basic_engine import __version__


setup(
    name="basic_engine",
    version=__version__,
    install_requires=[
        "numpy>=1.23.5",
        "shapely>=1.8.5",
    ],
    author="Spacewalk-tech",
    author_email="aa@spacewalk.tech",
    description="Basic Engine for Grasshopper",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)

print(find_packages(where='src'))
