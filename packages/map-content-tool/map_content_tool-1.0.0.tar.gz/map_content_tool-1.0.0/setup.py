from setuptools import setup

setup(
    name="map-content-tool",
    version="1.0.0",
    py_modules=["mapContentTool"],
    install_requires=[], 
    entry_points={
        "console_scripts": [
            "map-content=mapContentTool:main",
        ],
    },
    author="Housam Kak",
    author_email="housam.kak20@gmail.com",
    description="A tool to map directory contents and save output as TXT or JSON.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HousamKak/map-content-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)
