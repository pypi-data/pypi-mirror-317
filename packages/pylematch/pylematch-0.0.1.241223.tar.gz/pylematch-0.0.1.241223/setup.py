from setuptools import setup, find_packages

setup(
    name="Pylematch",
    version="0.0.1.241223",
    description="A module for matching file system paths against patterns.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Andrii Burkatskyi aka andr11b",
    author_email="4ndr116@gmail.com",
    url="https://github.com/codyverse/pylematch",
    license="MIT",
    packages=find_packages(include=["pylematch"]),
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=6.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
