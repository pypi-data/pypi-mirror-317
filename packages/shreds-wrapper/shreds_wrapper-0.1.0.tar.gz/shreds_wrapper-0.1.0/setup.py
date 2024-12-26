from setuptools import setup, find_packages

setup(
    name="shreds_wrapper",  # Replace with your package name
    version="0.1.0",
    author="shed skins",
    author_email="newerbandit@proton.me",
    description=" a sample pypi package.please do not install",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/njeru-codes/hello-pip",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
