
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('LICENSE') as f:
    lic = f.read()

setup(
    name='develop_tools',
    version='1.2.0',
    author='Rupert Hußnätter',
    author_email='',
    description='python scripts useful for python development',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/javatechy/dokr",
    zip_safe=True,
    license=lic,
    packages=find_packages('src'),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        "console_scripts":
            ['new_package=dev_tools.create_package:main']
    },
    install_requires=[
        "setuptools<=75.6.0"

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
