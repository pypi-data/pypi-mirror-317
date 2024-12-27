from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="octopus-dash",
    version="0.0.1",
    author="Hussein Naeem",
    author_email="husseinnaeemsec@gmail.com",
    description="A Dynamic better UI Django Dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/husseinnaeemsec/octopus-dash",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=[
        'Django>=3.2',
        # Add other dependencies
    ],
    include_package_data=True,
)