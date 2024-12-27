from setuptools import setup, find_packages

setup(
    name="data_analysis_tool",
    version="0.1",
    packages=find_packages(),
    author="Your Name",
    author_email="your_email@example.com",
    description="A tool for data analysis and visualization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/data_analysis_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "matplotlib",
        "csv"
    ]
)