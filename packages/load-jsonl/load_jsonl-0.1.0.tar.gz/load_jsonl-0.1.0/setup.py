from setuptools import setup, find_packages

setup(
    name="load_jsonl",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Ignora",
    author_email="tanz@mail.ustc.edu.cn",
    description="A simple JSONL file loader",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)