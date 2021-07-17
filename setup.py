from setuptools import setup, find_packages
import re

VERSION_FILE = "BundestagsAPy/__init__.py"
with open(VERSION_FILE) as version_file:
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                      version_file.read(), re.MULTILINE)

if match:
    version = match.group(1)
else:
    raise RuntimeError(f"Unable to find version string in {VERSION_FILE}.")

with open("README.md") as readme_file:
    long_description = readme_file.read()

# Setting up
setup(
        name="BundestagsAPy", 
        version=version,
        author="Paul Bose",
        author_email="<bose@ese.eur.nl>",
        description='Python Wrapper for the Bundestags API',
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=["requests>=2.26.0,<3",],
    
        keywords=['Bundestag','API'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3.7",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)