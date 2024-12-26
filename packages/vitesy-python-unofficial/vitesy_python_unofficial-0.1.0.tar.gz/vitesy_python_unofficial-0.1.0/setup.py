from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="vitesy-python-unofficial",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=1.8.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Unofficial Python SDK for Vitesy APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vitesy-python-unofficial",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
) 