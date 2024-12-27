from setuptools import setup, find_packages

setup(
    name="rm_onelineai",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "google-generativeai",
        "anthropic"
    ],
    author="Rohit Mane",
    author_email="rohitmane2001@gmail.com",
    description="A Python module for interacting with various AI models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rm_onelineai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)