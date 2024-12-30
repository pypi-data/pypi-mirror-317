from setuptools import setup, find_packages

setup(
    name="iniknumber",  # Use a valid name (lowercase, no spaces, underscores or dashes allowed)
    version="0.1.0",  # Ensure the version is in X.Y.Z format
    description="A Python package for parsing and validating NIK numbers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="irwannafly13",
    author_email="anggadventurez@gmail.com",
    url="https://github.com/yourusername/iniknumber",  # Correct URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
    ],
    package_data={
        "iniknumber": ["data/*.csv"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
