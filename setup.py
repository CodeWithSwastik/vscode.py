from setuptools import setup, find_packages

version = "1.5.3"
 
with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

with open("vscode/main.js", "r", encoding="utf-8") as js_file:
    data = f"'''{js_file.read()}'''"

with open("vscode/data.py", "w", encoding="utf-8") as data_py:
    data_py.write(data)

setup(
    name="vscode-ext",
    version=version,
    description="Create VSCode Extensions with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Swas.py",
    author_email="cwswas.py@gmail.com",
    packages=find_packages(),
    url = "https://github.com/CodeWithSwastik/vscode-ext", 
    project_urls={
    "Issue tracker": "https://github.com/CodeWithSwastik/vscode-ext/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    install_requires=[],
    python_requires=">=3.6",
)
