from setuptools import setup, find_packages

setup(
    name="telenotif",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot>=20.0",
    ],
    author="Sina",
    author_email="sina7th@gmail.com",
    description="A simple notification library using Telegram bots",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)