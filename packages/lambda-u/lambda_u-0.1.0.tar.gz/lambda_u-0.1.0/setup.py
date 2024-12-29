from setuptools import setup, find_packages

setup(
    name="lambda_u",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Soul2024tk",
    author_email="soulcodingyanhun@gmail.com",
    description="Python lambda extension library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Soul2024tk/lambda",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 