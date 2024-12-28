from setuptools import setup, find_packages

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
]

setup(
    name="pylitter",
    version="1.1.1",
    packages=find_packages(),
    author="moisentinel, yukinotenshi",
    author_email="nibir@nibirsan.org, gabriel.bentara@gmail.com",
    license="MIT",
    url="https://github.com/moiSentineL/litter",
    install_requires=["requests", "requests-toolbelt", "click"],
    description="CLI tool to upload file to litterbox/catbox",
    keywords="direct upload cli",
    classifiers=CLASSIFIERS,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": ["throw=litter.main:cli", "litter=litter.main:cli"]
    },
)
