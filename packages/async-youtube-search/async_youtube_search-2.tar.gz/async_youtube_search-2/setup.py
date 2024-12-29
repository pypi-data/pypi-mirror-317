import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="async-youtube-search",
    version="2",
    description="Perform YouTube video searches without the API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rafkix/async-youtube-search",
    author="Rafkix",
    author_email="rafkixuz@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.13",
    ],
    packages=["async_youtube_search"],
    include_package_data=True,
    install_requires=["requests"],
)
