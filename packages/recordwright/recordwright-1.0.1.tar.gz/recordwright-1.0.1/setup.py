"""Recordwright"""
import os
from setuptools import setup, find_namespace_packages

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


options = {
    "install_requires": [
        "playwright",
    ],
    "include_package_data": True,
    "package_data": {
        "recordwright": ["*.js"],
    }
}

setup(
    name="recordwright",
    version="1.0.1",
    package_dir={'': 'src'},
    packages=find_namespace_packages(where="src"),
    author="Michael Reithinger",
    author_email="mreithinger@web.de",
    description="An extension for recording and playback of web interactions in Playwright",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    license="MIT",
    keywords="library,testing,development,web",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Testing"],
    url="https://github.com/kochelmonster/recordwright",
    **options
)
