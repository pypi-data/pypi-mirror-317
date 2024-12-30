from setuptools import setup, find_packages

setup(
    name="imagery24",
    version="0.2.0",
    packages=find_packages(),
    description="A short description of your package",
    long_description_content_type="text/markdown",
    author_email="your.email@example.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "rasterio",
        "Pillow",
        "tifffile",
    ],
    zip_safe=True,
)
