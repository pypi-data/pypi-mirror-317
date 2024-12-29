from setuptools import setup, find_packages

setup(
    name="get_buildings",
    version="0.1.4",
    author="Araz Shah",
    author_email="araz.shah@gmail.com",
    description="A tool for downloading and processing building footprints using bounding box data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/arazshah/get_buildings",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "shapely",
        "geopandas",
        "mercantile",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "get_buildings=get_buildings:main",
        ],
    },
)
