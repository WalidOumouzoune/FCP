import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="pfcp",
    version="0.0.2",
    author="Walid OUMOUZOUNE",
    author_email="walid.amozon@gmail.com",
    description=("Track football game form terminal"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/walidOumouzoune/PFC",
    project_urls={
        "Bug Tracker": "https://github.com/walidOumouzoune/FCP/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "tabulate", "pyfiglet"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "FCP = FCPpk.cli:main",
        ]
    }
)