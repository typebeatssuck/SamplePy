"""
Setup script for SamplePy
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="samplepy",
    version="1.0.0",
    author="SamplePy Team",
    author_email="team@samplepy.com",
    description="A powerful CLI tool for bulk audio operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samplepy/samplepy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pydub>=0.25.1",
        "mutagen>=1.46.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "spy=samplepy.main:app",
        ],
    },
    keywords="audio, conversion, metadata, organization, cli, bulk-processing",
    project_urls={
        "Bug Reports": "https://github.com/samplepy/samplepy/issues",
        "Source": "https://github.com/samplepy/samplepy",
        "Documentation": "https://github.com/samplepy/samplepy#readme",
    },
) 