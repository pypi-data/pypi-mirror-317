from setuptools import setup, find_packages

setup(
    name="fast_trie_set",
    version="0.6.1",
    description="A fast and efficient trie-based collection for storing and searching millions of strings.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Yashraj Singh Rawat",
    author_email="yashraj22august@gmail.com",
    url="https://github.com/YashrajSinghRawat/fast_trie",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
