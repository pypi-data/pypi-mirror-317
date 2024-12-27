from setuptools import setup, find_packages

setup(
    name="Deciml",
    version="0.1.0",
    description="Extension of Decimal standard package",
    author="Shank",
    author_email="kor.shantanu1@gmail.com",
    url="https://github.com/shantanu-kor/Deciml.git",
    packages=find_packages(),
    install_requires=[
        # List dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
