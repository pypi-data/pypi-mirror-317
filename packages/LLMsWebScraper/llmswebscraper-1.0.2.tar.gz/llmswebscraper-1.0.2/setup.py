import setuptools
import subprocess
import os

LLMsWebScraper_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

if "-" in LLMsWebScraper_version:
    # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
    # pip has gotten strict with version numbers
    # so change it to: "1.3.3+22.git.gdf81228"
    # See: https://peps.python.org/pep-0440/#local-version-segments
    v, i, s = LLMsWebScraper_version.split("-")
    LLMsWebScraper_version = v + "+" + i + ".git." + s

assert "-" not in LLMsWebScraper_version
assert "." in LLMsWebScraper_version

assert os.path.isfile("LLMsWebScraper/version.py")
with open("LLMsWebScraper/VERSION", "w", encoding="utf-8") as fh:
    fh.write("%s\n" % LLMsWebScraper_version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LLMsWebScraper",
    version=LLMsWebScraper_version,
    author="Kavindu Deshappriya",
    author_email="ksdeshappriya.official@gmail.com",
    description="A Python library to extract structured data from web pages using LLMs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KSDeshappriya/LLMsWebScraper-pip.git",
    packages=setuptools.find_packages(),
    package_data={"LLMsWebScraper": ["VERSION"]},
    include_package_data=True,
    install_requires=[
        "requests>=2.32.3",
        "retrying>=1.3.4",
        "python-dotenv>=1.0.1",
        "langchain>=0.3.13",
        "langchain-community>=0.3.13",
        "langchain-google-genai>=2.0.7",
        "langchain-groq>=0.2.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
