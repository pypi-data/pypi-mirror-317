import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastapi_boot",
    version="0.0.3",
    author="hfdy0935",
    author_email="",
    description="FastAPI development toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/hfdy0935/fastapi_boot",
    project_urls={"Repository": "https://github.com/hfdy0935/fastapi_boot"},
    packages=setuptools.find_packages(),
    install_requires=[
        "starlette>=0.40.0,<0.42.0",
        "pydantic>=1.7.4,!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0",
        "typing-extensions>=4.8.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
