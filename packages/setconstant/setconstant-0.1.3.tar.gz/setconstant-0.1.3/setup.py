from setuptools import setup, find_packages

setup(
    name="setconstant",  # The name of your package
    version="0.1.3",  # The initial version of your package
    author="Anuraj R",  # Your name
    author_email="anurajanu2883@gmail.com",  # Your email address
    description="A Python package for managing constants effectively.",  # Short description
    long_description=open("README.md", encoding="utf-8").read(),  # Detailed description from README.md
    long_description_content_type="text/markdown",  # README.md is written in Markdown
    url="https://github.com/Anuraj-CodeHaven",  # Link to your GitHub repository
    packages=find_packages(),  # Automatically find all packages in the current directory
    classifiers=[
        "Programming Language :: Python :: 3",  # Supported programming language
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",  # OS compatibility
    ],
    python_requires=">=3.6",  # Minimum Python version required
)
