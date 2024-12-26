from setuptools import setup, find_packages


def find_required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="jj-spec-validator",
    version="1.0.0",
    description="jj mocks validator for openapi specs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sam Roz",
    author_email="rolez777@gmail.com",
    python_requires=">=3.10",
    url="https://github.com/Maestoz/jj-spec-validator",
    license="Apache-2.0",
    packages=find_packages(),
    install_requires=find_required(),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ]
)
