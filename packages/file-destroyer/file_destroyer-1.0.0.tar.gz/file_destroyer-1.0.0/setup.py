from setuptools import setup, find_packages

setup(
    name="file_destroyer",
    version="1.0.0",
    author="Abhi pratap singh",
    author_email="Abhi.pratap9667@gmail.com",
    description="A GUI tool to permanently destroy files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Abhipratapsingh123/File_destroyer",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt6",
    ],
    entry_points={
        "console_scripts": [
            "file-destroyer=file_destroyer.file_destroyer:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
