from setuptools import find_packages, setup

setup(
    name="syncmaster-commons",  # Package name
    version="0.0.26",    # Initial version
    author="nakulben",
    author_email="tech@jinacode.systems",
    description="A core library for syncmaster.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jain-t/syncmaster-commons",  # Project URL
    packages=find_packages(),  # Automatically find packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
    install_requires=[
       "pydantic",
       "setuptools",
       "pytest"
    ],
)
