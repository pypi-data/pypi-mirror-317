from setuptools import setup, find_packages

setup(
    name="lukhed_basic_utils",
    version="0.2.0",
    description="A collection of basic utility functions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="lukhed",
    author_email="lukhed.mail@gmail.com",
    url="https://github.com/lukhed/lukhed_basic_utils",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pytz>=2024.2",
        "python-dateutil>=2.9.0",
    ],
)