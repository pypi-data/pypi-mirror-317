import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "durkinza.cdk-networkfirewall-l2",
    "version": "0.1.1",
    "description": "AWS CDK L2 constructs for the AWS Network Firewall (AWS::NetworkFirewall)",
    "license": "Apache-2.0",
    "url": "https://github.com/durkinza/cdk-networkfirewall-l2#readme",
    "long_description_content_type": "text/markdown",
    "author": "durkinza<8985088+durkinza@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/durkinza/cdk-networkfirewall-l2.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "durkinza.cdk_networkfirewall_l2",
        "durkinza.cdk_networkfirewall_l2._jsii"
    ],
    "package_data": {
        "durkinza.cdk_networkfirewall_l2._jsii": [
            "cdk-networkfirewall-l2@0.1.1.jsii.tgz"
        ],
        "durkinza.cdk_networkfirewall_l2": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.173.2, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
