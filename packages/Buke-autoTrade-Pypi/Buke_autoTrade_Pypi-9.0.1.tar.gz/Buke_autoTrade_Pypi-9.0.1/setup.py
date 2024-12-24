from setuptools import setup, find_packages

from setuptools import setup, find_packages

setup(
    name="Buke_autoTrade_Pypi",
    version="9.0.1",
    author="zaza011",
    author_email="yesben@naver.com",
    description="test source",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://eu4ng.tistory.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)