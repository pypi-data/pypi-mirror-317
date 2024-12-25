import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mysqlchain",
    version="1.2",
    author="LingFeng",
    author_email="418155641@qq.com",
    description="chain operation mysql database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.kancloud.cn/lingfengcms/mysqlchain/2646275",
    packages=setuptools.find_packages(),
    install_requires=['PyMySQL>=1.0.2'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)