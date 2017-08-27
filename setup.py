from setuptools import setup
import os

rootFolder = 'colouringmap'
pac_dirs = [ dirPath for dirPath, dirNames, fileNames in os.walk(rootFolder) ]

setup(
    name="colouringmap",

    version="0.0.3",
    
    author="Benny Chin",
    author_email="wcchin.88@gmail.com",
    
    packages= pac_dirs,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.ttf'],
    },
    #include_package_data=True,

    url="https://github.com/wcchin/colouringmap",

    license="LICENSE.txt",
    description="a mapping tool for generating choropleth map from map data (shpfile), by breaking sequential values into groups, or beforehand prepared category/level.",

    long_description=open("README.md").read(),
    
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Visualization',

         'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='map, geography, catography, thematic map',

    install_requires=[
        "numpy",
        "jenkspy",
        "palettable",
        "geopandas",
        "descartes",
        "matplotlib_scalebar",
    ],
)
