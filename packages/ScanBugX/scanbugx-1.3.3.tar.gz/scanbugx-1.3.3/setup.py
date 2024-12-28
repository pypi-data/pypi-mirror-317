from setuptools import setup, find_packages

# Read the README file for a long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ScanBugX",
    version="1.3.3",  # Semantic versioning: major.minor
    author="Ayan Rajpoot",
    author_email="ayanrajpoot2004@gmail.com",
    description="All in one toolkit for network analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ayanrajpoot10/BugScanX",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[

    ],
    entry_points={
        # Define your command-line tool here
        "console_scripts": [
            "bugscanx=bugscanx.main:main_menu",
        ],
    },
    license="MIT",
)
