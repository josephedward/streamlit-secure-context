 from setuptools import setup, find_packages

 setup(
     name="secure_ml_component",
     version="0.1.0",
     packages=find_packages(),
     include_package_data=True,
    install_requires=["streamlit>=0.63"],
    description="Secure ML Inference Streamlit Component",
    author="Edward Joseph",
    license="MIT",
 )