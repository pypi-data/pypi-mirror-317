from setuptools import setup, find_packages

VERSION = "0.0.3"
DESCRIPTION = "My first Python package"
LONG_DESCRIPTION = "Used for to create the documentation"


setup(
    name="mydocs-streamlit",
    version=VERSION,
    author="Jaswanth Anupoju",
    author_email="ajaswanth791@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="https://github.com/ajaswanth791/mydocs.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.40.0"
    ],
    entry_points={
        "console_scripts": [
            "mydocs=mydocs.running:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
