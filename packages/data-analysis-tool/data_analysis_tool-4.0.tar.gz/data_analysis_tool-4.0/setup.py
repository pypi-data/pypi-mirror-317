from setuptools import setup, find_packages

setup(
    name="data_analysis_tool",
    version="4.0",
    packages=find_packages(),
    author="xinyichen",
    author_email="your_email@example.com",
    description="A tool for data analysis and visualization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anniechan/data_analysis_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "matplotlib",
    ]
)