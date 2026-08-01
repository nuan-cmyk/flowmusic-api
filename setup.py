from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flowmusic-api",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An unofficial Python client for Flow Music API (flowmusic.app)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flowmusicapi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "pydantic>=2.4.2",
        "sseclient-py>=1.8.0"
    ],
)
