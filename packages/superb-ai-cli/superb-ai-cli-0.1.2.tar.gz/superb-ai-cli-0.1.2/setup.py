import io
import json
from setuptools import setup, find_packages


def long_description():
    with io.open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


def load_config():
    with io.open('./spb_cli/config.json', 'r', encoding='utf-8') as fid:
        return json.load(fid)


configs = load_config()
setup(
    name=configs["CLI_NAME"],
    version=configs["CLI_VERSION"],
    url=configs["CLI_URL"],
    license=configs["CLI_LICENSE"],
    author=configs["CLI_AUTHOR"],
    author_email=configs["CLI_AUTHOR_EMAIL"],
    description="Superb Platform CLI",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["superb=spb_cli.__main__:cli"]},
    long_description=long_description(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={
        "spb_cli": ["*.json"],
    },
    install_requires=[
        "click",
        "requests",
        "superb-ai-label"
    ],
    zip_safe=False,
    dependency_links=[],
)
