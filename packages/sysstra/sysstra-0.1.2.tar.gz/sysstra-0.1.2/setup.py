from setuptools import setup, find_packages

setup(
    name="sysstra",  # Your package name (must be unique on PyPI)
    version="0.1.2",  # Initial release version
    description="Official Python Library for Sysstra Algo Trading",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Anurag Singh Kushwah",
    author_email="anurag786kushwah@gmail.com",
    url="https://github.com/sysstra/sysstra",  # Link to source code
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[  # Dependencies
        "requests",
        "numpy",
        "pandas_ta",
        "redis",
    ],
    classifiers=[  # Additional metadata (check PyPI classifiers)
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)