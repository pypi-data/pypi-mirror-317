from setuptools import setup

# Read the long description from README.md if it exists
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A tool to map directory contents and save output as TXT or JSON."

setup(
    name="map-content-tool",
    version="1.2.0",
    py_modules=["mapContentTool"],
    install_requires=[
        "urwid>=2.1.2",  # Third-party dependency
    ],
    entry_points={
        "console_scripts": [
            "map-content=mapContentTool:main",
        ],
    },
    author="Housam Kak",
    author_email="housam.kak20@gmail.com",
    description="A tool to map directory contents and save output as TXT or JSON.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HousamKak/map-content-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)
