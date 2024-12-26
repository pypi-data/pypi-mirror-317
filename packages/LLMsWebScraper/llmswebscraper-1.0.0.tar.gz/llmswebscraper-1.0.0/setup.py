from setuptools import setup, find_packages

setup(
    name="LLMsWebScraper",
    version="1.0.0",
    author="Kavindu Deshappriya",
    author_email="ksdeshappriya.official@gmail.com",
    description="A Python library to extract structured data from web pages using LLMs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KSDeshappriya/LLMsWebScraper-pip.git",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "retrying>=1.3.4",
        "python-dotenv>=1.0.1",
        "google-generativeai>=0.8.3",
        "langchain>=0.3.13",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
