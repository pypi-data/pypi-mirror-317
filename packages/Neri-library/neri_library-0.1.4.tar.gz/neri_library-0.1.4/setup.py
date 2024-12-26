from setuptools import setup, find_packages

setup(
    name="Neri_library",
    version="0.1.4",
    author="Neri",
    author_email="gui.neriaz@gmail.com",
    description="Me segue no insta ae @_._neri",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
    "undetected-chromedriver",
    "selenium-stealth",
    "setuptools"
    "selenium",
    "requests",
    ],
)
