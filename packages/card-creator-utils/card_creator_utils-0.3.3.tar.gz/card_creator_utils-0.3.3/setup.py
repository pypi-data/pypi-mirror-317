from setuptools import setup, find_packages

setup(
    name="card-creator-utils",
    version="0.3.3",
    packages=find_packages(),
    install_requires=[
        "Pillow>=10.3.0",
        "reportlab>=4.2.0",
        # add other dependencies here
    ],
    author="Simon Gheeraert",
    author_email="simon.gheeraert.sg@gmail.com",
    description="A utility package for creating cards (including for board games) with images and text",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/simonghrt/card-creator-utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
