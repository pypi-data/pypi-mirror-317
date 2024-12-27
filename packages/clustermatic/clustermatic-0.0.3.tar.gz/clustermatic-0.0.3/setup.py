from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
    required = f.read().splitlines()


setup(
    name="clustermatic",
    version="0.0.3",
    packages=find_packages(),
    install_requires=required,
    package_data={
        "clustermatic": ["auxiliary/*"],
    },
    include_package_data=True,
    description="Python AutoML library for clustering tasks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aleks Kapich",
    author_email="aleks.kapich@gmail.com",
    url="https://github.com/AKapich/clustermatic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
