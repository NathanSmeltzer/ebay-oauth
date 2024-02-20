import setuptools

with open("README.adoc", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ebay-oauth",
    packages=setuptools.find_packages(),
    version="0.0.5",
    description="eBay Oauth Client ShipAware Fork",
    long_description=long_description,
    author="Logistero Ltd dba ShipAware",
    author_email="nathan.smeltzer@gmail.com",
    url="https://github.com/NathanSmeltzer/ebay-oauth",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: Other/Proprietary License",
    ],
    python_requires='>=3.7',)