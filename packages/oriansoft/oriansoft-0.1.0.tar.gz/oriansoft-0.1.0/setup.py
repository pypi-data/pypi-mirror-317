from setuptools import setup, find_packages

setup(
    name="oriansoft",
    version="0.1.0",
    author="OrianSoft",
    author_email="info@oriansoft.com",
    description="All py functions are defined in this package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires=">=3.6",
)
