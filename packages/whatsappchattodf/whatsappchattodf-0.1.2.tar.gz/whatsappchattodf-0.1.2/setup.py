from setuptools import find_packages, setup

setup(
    name="whatsappchattodf",
    version="0.1.2",
    author="Kartheek Palepu",
    author_email="kartheekpnsn@gmail.com",
    description="Convert WhatsApp chat logs (.txt) to a pandas DataFrame.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kartheekpnsn/whatsappchattodf",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "whatsappchattodf=whatsappchattodf.whatsappchattodf:main",
        ],
    },
)
