import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-your-username",
    version="0.0.1",
    author="Marco Pavanelli",
    author_email="marco.pavanelli@sasabz.it",
    description="This is an esperimental library to send email using Microsoft Graph API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/azure_simple_email",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)