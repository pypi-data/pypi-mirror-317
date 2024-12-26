from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.1'
DESCRIPTION = 'Fetch stock data via Google Finance'
LONG_DESCRIPTION = 'A package that fetched data about stocks listed on NSE, BSE, NYSE, NASDAQ, etc.'

# Setting up
setup(
    name="stocksnap",
    version=VERSION,
    author="Om Rawal",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author_email = 'omrawal2801@gmail.com',
    url = 'https://github.com/omrawal/Stock-Snap', 
    packages=find_packages(),
    include_package_data=True,
    install_requires=['beautifulsoup4', 'requests', 'bs4','urllib3'],
    keywords=['python', 'stock', 'BSE', 'API', 'NSE', 'scraping', 'web scraping'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)