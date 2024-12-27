from setuptools import setup, find_packages

setup(
    name="amangee",
    version="0.2.2",
    description="A Python library for GEE, AI, and hydrology applications.",
    long_description="Amangee is a comprehensive Python library designed for hydrology, "
                     "AI integration, and Google Earth Engine applications. It provides "
                     "tools for watershed delineation, river network extraction, "
                     "and advanced geospatial visualization.",
    long_description_content_type="text/markdown",  # Use Markdown for long description
    author="Chakapp",
    author_email="chakapp2424@example.com",
    url="https://github.com/yourusername/amangee",  # Replace with your GitHub repo
    packages=find_packages(),  # Automatically finds your modules
    install_requires=[
        "numpy",
        "pandas",
        "geopandas",
        "folium",
        "matplotlib",
        "rasterio",
        "shapely",
        "scipy",
        "pysheds",
    ],
    python_requires=">=3.7",  # Specify Python version compatibility
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Specify your license
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: GIS",
        "Intended Audience :: Science/Research",
    ],
    keywords="hydrology gee ai watershed python geospatial",
    license="MIT",  # Replace with your license if different
)
