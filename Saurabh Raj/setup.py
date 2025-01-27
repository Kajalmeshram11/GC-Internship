#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name="google-scraper",
    version="0.1.0",
    description="A Google search results scraper using Selenium",
    long_description=open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
    ).read(),
    long_description_content_type="text/markdown",
    author="Saurabh Raj",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "webdriver_manager",
        "docopt",
        "colorful",
    ],
    entry_points={
        "console_scripts": [
            "google-scraper=google_scraper.main:main"
        ]
    },
)