from setuptools import setup, find_packages

setup(
    name="TitlesArt",
    version="1.0.3",
    description="Create titles for command-line tools easily.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Pachi",
    author_email="pachoof345@gmail.com",
    url="https://github.com/PACHOOF/TitlesArt.git",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
