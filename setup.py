import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hyperspy_swift_library",
    version="0.1",
    author="francisco-dlp",
    author_email="francisco.de-la-pena-manchon@univ-lille.fr",
    description="Read Nion Swift library with HyperSpy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hyperspy/hyperspy_swift_libray",
    packages=setuptools.find_packages(),
    install_requires=["nionswift>0.14"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
