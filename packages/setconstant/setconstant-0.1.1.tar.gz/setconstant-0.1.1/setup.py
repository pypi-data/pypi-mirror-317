from setuptools import setup, find_packages

setup(
    name="setconstant",                 
    version="0.1.1",                   
    author="Anuraj R",
    author_email="anurajanu2883@gmail.com",
    description="A module for managing constants",
    packages=find_packages(),           # Automatically find package directories
    install_requires=[],                # List of dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
