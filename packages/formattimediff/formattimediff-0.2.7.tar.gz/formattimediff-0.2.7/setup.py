from setuptools import setup, find_packages
import datetime

setup(
    name="formattimediff",
    version="0.2.7",
    packages=find_packages(),
    install_requires=[
        "datetime"
    ],
    author="Datascripter",
    author_email="cody@datascripter.com",
    description="Simple quick formatting of time differences",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Datascripter/FormatTimeDiff",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
)
