from setuptools import setup, find_packages

setup(
    name="meteopoint",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "typer>=0.9.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "argcomplete>=3.2.1"
    ],
    entry_points={
        "console_scripts": [
            "meteopoint=meteopoint.meteopoint:app",
        ],
    },
    author="MeteoPoint Contributors",
    author_email="your.email@example.com",
    description="A beautiful CLI tool for weather and environmental data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/meteopoint",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
) 