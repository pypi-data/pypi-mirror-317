from setuptools import setup, find_packages

setup(
    name="sipametrics",
    version="0.1.1",
    description="Scientific Infra & Private Assets",
    long_description=open("README.rst").read(),
    long_description_content_type="text/markdown",
    author="SIPA",
    author_email="support@scientificinfra.com",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
