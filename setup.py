"""
Setup script for pyOxygenSCPI

@author: Matthias Straka <matthias.straka@dewetron.com>
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyOxygenStream",
    version="0.0.1",
    author="Michael Oberhofer",
    author_email="michael.oberhofer@dewetron.com",
    description="Python library for live data streaming from Dewetron Oxygen",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DEWETRON/pyOxygenStream",
    keywords='Measurement, Signal processing, Storage, Streaming',
    project_urls={
        "Bug Tracker": "https://github.com/DEWETRON/pyOxygenStream/issues",
        "Source Code": "https://github.com/DEWETRON/pyOxygenStream",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platforms=["Windows", "Linux"],
    packages=["pyOxygenStream"],
    package_dir={"pyOxygenStream": "pyOxygenStream"},
    install_requires=[],
    python_requires=">=3.6",
)
