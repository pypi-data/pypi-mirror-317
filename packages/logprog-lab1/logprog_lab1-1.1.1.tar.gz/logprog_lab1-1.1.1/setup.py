from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(
    name="logprog_lab1",
    version="1.1.1",
    description="logprog_lab1",
    author="regina_mikhailova",
    author_email="riga157@mail.ru",
    url="https://github.com/tesllaaa/logprog_lab1",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
)
