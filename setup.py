import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyservice",  # Replace with your own username
    version="0.0.3",
    author="Attila Domokos",
    author_email="adomokos@gmail.com",
    description="Series of Actions with an emphasis on simplicity.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adomokos/pyservice",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
