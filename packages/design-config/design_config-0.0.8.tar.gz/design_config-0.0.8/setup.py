import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "design_config",
    version = "0.0.8",
    author = "Artem Antonov",
    author_email = "artmihant@gmail.com",
    description = "Smart tiny config library for flask-like config",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/artmihant/design_config",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers"
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)