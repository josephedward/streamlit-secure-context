 from setuptools import setup, find_packages

 setup(
    name="streamlit-secure-context",
     version="0.1.1",
     packages=find_packages(),
     include_package_data=True,
    install_requires=["streamlit>=0.63"],
    description="Streamlit Secure Context Component",
    author="Edward Joseph",
    license="MIT",
 )
