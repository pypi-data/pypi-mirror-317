from setuptools import setup, find_packages

setup(
    name="pmtk",  
    version="0.1.4",  
    description="A package providing project management tools like NetworkDiagram and NetworkDiagramExporter.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Yasayah-Nadeem-Khokhar/pmtk",
    author="Yasayah Nadeem Khokhar",
    author_email="yasayahnadeem22@gmail.com",
    license="MIT",
    packages=find_packages(),  
    install_requires=["pandas"],  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
