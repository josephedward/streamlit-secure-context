from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
from pathlib import Path

# Load the long description from README.md
long_description = Path(__file__).parent.joinpath("README.md").read_text(encoding="utf-8")

setup(
    name="streamlit-secure-context",
     version="0.1.2",
     packages=find_packages(),
     include_package_data=True,
    install_requires=["streamlit>=0.63"],
    description="Streamlit Secure Context Component",
    long_description=long_description,
    long_description_content_type="text/markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Edward Joseph",
    license="MIT",
 )
