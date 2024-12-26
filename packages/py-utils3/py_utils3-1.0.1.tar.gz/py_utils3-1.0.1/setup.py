from setuptools import setup, find_packages

setup(
    name="py-utils3",
    version="1.0.1",
    author="MohamedLunar",
    author_email="contact.mohamedlunardev@gmail.com",
    description="🔗 Package Guide On https://github.com/mohamedlunar/py-utils3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mohamedlunar/py-utils3",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
