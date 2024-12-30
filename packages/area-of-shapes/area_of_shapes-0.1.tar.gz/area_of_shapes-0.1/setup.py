from setuptools import setup, find_packages

setup(
    name='area_of_shapes',
    version='0.1',
    author= "Amaechi Ugwu",
    author_email="amaechijude178@gmail.com",
    description="A simple python package to calculate the area of different shapes",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/amaechijude/area",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)