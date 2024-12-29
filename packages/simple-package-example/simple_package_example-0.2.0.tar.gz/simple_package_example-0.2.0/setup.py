from setuptools import setup, find_packages

setup(
    name="simple-package-example",  # Unique name on PyPI
    version="0.2.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple package to greet users.",
    long_description='long description',
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/simple_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)