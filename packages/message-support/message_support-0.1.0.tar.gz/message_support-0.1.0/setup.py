from setuptools import setup, find_packages

setup(
    name="message-support",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    description="Python library for interacting with message.support's API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Message.Support",
    url="https://message.support",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
