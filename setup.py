import setuptools

with open("README.adoc", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ebay-oauth",
    packages=setuptools.find_packages(),
    version="0.0.2",
    description="eBay Oauth Client",
    long_description=long_description,
    author="Market Math LLC",
    author_email="nathan.smeltzer@gmail.com",
    url="https://gitlab.com/Smeltzer/ebay-oauth",
    download_url="https://gitlab.com/Smeltzer/ebay-oauth/-/archive/master/selenium-browser-shopper-master.zip",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: Other/Proprietary License",
    ],
    python_requires='>=3.6',)