from setuptools import setup, find_packages

setup(
    name="metatool",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-core",
        "langchain-community",
        "langchain-openai",
        "pydantic",
        "open-interpreter",
        "uuid"
    ],
    author="James Zhang",
    description="A Python interface for metatool functionality",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
)
