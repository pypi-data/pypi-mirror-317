import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloud-duck",
    "version": "0.0.12",
    "description": "CDK construct for creating an analysis environment using DuckDB for S3 data",
    "license": "Apache-2.0",
    "url": "https://github.com/badmintoncryer/cloud-duck.git",
    "long_description_content_type": "text/markdown",
    "author": "Kazuho CryerShinozuka<malaysia.cryer@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/badmintoncryer/cloud-duck.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cloud-duck",
        "cloud-duck._jsii"
    ],
    "package_data": {
        "cloud-duck._jsii": [
            "cloud-duck@0.0.12.jsii.tgz"
        ],
        "cloud-duck": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.160.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "deploy-time-build>=0.3.23, <0.4.0",
        "jsii>=1.106.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
