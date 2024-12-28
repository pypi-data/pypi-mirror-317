from setuptools import setup, find_packages

setup(
    name="ogmsgui",
    version="0.1.5",
    author="Phileon Ma",
    author_email="mpllonggis@gmail.com",
    description="A GUI package for geographical modeling and simulation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MPLebron/ogmsgui",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'ogmsgui': ['data/*.json'],
    },
    install_requires=[
        'ipywidgets',
        'ipyfilechooser',
        'requests',
        'markdown',
        'nest_asyncio',
        'openai',
        'asyncio'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)