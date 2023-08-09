import setuptools

REQUIRED_PACKAGES = ['python-binance==1.0.18']

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ffautomaton_binance_service",
    version="1.0",
    author="FFAutomaton",
    author_email="ffautomaton@yahoo.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FFAutomaton/service-binance-rest",
    install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
