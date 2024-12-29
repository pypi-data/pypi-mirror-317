from setuptools import setup, find_packages

setup(
    name="git-installer",
    version="0.1.0",
    description="Python library to detect and install Git across different platforms.",
    author="Dominik Průša",
    author_email="domino@let.email",
    url="https://github.com/DominoPrusa/python-git-installer",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT or WTFPL",
)