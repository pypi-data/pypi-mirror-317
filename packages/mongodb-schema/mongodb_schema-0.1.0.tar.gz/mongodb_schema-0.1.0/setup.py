from setuptools import setup, find_packages

setup(
    name="mongodb-schema",
    version="0.1.0",
    description="A Python SDK for exporting MongoDB schema metadata",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Karan Bhatia",
    author_email="karanbhatia.kb27@gmail.com",
    url="https://github.com/karanbhatiakb/mongodb-schema/tree/master",
    packages=find_packages(),
    install_requires=["pymongo"],
    entry_points={
        "console_scripts": [
            "mongodb-schema=mongodb_schema.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
