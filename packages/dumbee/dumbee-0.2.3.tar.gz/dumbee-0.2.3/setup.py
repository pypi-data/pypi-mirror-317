import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dumbee",
    version="0.2.3",
    author="David Schenck",
    author_email="david.schenck@outlook.com",
    description="A dumb database, not for production",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dschenck/dumbee",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["jsonschema", "pydantic", "filelock"],
    include_package_data=True,
)
