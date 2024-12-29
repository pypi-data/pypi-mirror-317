from setuptools import setup, find_packages

setup(
    name="rotools",
    version='0.1.64',
    author="Robert Olechowski",
    author_email="robertolechowski@gmail.com",
    description="Robert Olechowski python tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RobertOlechowski/ROTools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[],
)