from setuptools import setup, find_packages

setup(
    name="my_library_dnvb",
    version="0.1.0",
    description="A sample Python library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Lazarev Daniil",
    author_email="1132230808@pfur.ru",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
