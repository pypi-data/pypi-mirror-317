from setuptools import setup, find_packages

setup(
    name="langrs",
    version="0.1.5",
    author="Mohanad Diab",
    author_email="mdiab@eurac.edu",
    description="Remote sensing image segmentation using LangSAM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MohanadDiab/langrs",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "Pillow",
        "rasterio",
        "torch",
        "scipy",
        "scikit-learn",
        "segment-geospatial",
    ],

    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
