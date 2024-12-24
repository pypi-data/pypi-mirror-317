import setuptools

# Load the long_description from README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Han_BackTest",
    version="1.1.2",
    author="Jiaheng Han",
    author_email="hanjiaheng@stu.pku.edu.cn",
    description="A naive backtest framework for stock trading in Chinese market",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.linkedin.com/in/jiaheng-han-005464291",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)