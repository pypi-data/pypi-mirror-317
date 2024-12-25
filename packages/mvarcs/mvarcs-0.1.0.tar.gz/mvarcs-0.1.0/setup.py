import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mvarcs",
    version="0.1.0",
    author="OllieJC",
    author_email="mvarcs-pypi@olliejc.uk",
    description="Python package for providing the MVARCS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/markcerts/mvarcs-python",
    project_urls={
        "Bug Tracker": "https://github.com/markcerts/mvarcs-python/issues",
        "MVARCS": "https://github.com/markcerts/mvarcs",
    },
    license="The Unlicense",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    package_dir={"mvarcs": "src"},
    package_data={"mvarcs": ["mvarcs/*.pem"]},
    packages=["mvarcs"],
    python_requires=">=3.6",
)
