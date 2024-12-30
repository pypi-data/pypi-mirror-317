from setuptools import find_packages, setup

setup(
    name="tox-docker-id",
    description="Manage lifecycle of docker containers during Tox test runs (patched version)",
    long_description=open("README.rst").read(),
    url="https://github.com/d9pouces/tox-docker",
    maintainer="Matthieu Gallet",
    maintainer_email="github@19pouces.net",
    install_requires=[
        "docker>=4.0,<8.0",
        "tox>=4.0.0,<5.0",
    ],
    packages=find_packages(),
    entry_points={"tox": ["docker = tox_docker"]},
    vcversioner={"version_module_paths": ["_version.py"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Testing",
    ],
)
