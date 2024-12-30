from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="meteopoint",
    version="0.1.0",
    author="MeteoPoint Contributors",
    author_email="your.email@example.com",
    description="A beautiful CLI tool for weather and environmental data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/meteopoint",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    package_data={
        "meteopoint": ["py.typed"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
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
    install_requires=[
        "click==8.1.7",
        "requests==2.31.0",
        "python-dotenv==1.0.0",
        "rich==13.7.0",
        "typer==0.9.0",
        "argcomplete==3.2.1"
    ],
    entry_points={
        "console_scripts": [
            "meteopoint=meteopoint.meteopoint:app",
        ],
    },
) 