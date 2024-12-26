from setuptools import setup, find_packages

setup(
    name="mongo-schema-V2",
    version="0.1.4",
    description="A Python SDK for exporting MongoDB schema metadata",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Karan Bhatia",
    author_email="karanbhatia.kb27@gmail.com",
    url="https://github.com/karanbhatiakb/mongo-schema-V2/tree/master",
    packages=find_packages(),
    install_requires=["pymongo", "bson"],
    entry_points={
        "console_scripts": [
            "mongo-schema-V2=mongo_schema.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
