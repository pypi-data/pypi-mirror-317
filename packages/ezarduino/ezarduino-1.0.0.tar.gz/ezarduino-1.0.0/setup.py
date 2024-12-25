from setuptools import setup, find_packages

setup(
    name="ezarduino",
    version="1.0.0",
    packages=find_packages(),
    description="A library designed to facilitate communication between Python and Arduino devices.",
    author="Crate",
    author_email="crate.arg@proton.me",
    url='https://github.com/cr4t3/ezarduino',
    install_requires=[
        "pyserial>=3.5"
    ],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent"
    ]
)