from setuptools import setup, find_packages

setup(
    name="meteopoint",
    version="0.3.2",
    description="A simple CLI tool for weather and air quality data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="princemuichkine",
    author_email="",
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
    python_requires=">=3.7",
) 