from setuptools import setup, find_packages

setup(
    name="amangee",
    version="0.1",
    description="A Python library for GEE, AI, and hydrology applications.",
    author="Chakapp",
    author_email="chakapp2424@example.com",
    packages=find_packages(),  # Automatically finds your modules
    install_requires=[
        "numpy",           # Example dependencies
        "pandas",
        "earthengine-api",
    ],
    python_requires=">=3.7",    # Specify Python version compatibility
)

