from setuptools import setup, find_packages

setup(
    name="metasnake",
    version="1.0.0",
    author="Xing Chen",
    author_email="zsqing_chen@163.com",
    description="MetaSnake: A metagenomic Bioinformatics Workflow Powered by Snakemake",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/XingChen-zsq/Metasnake",  
    license="GPL-3.0",
    packages=find_packages(),  
    include_package_data=True,  
    install_requires=[
        "snakemake",
    ],
    entry_points={
        "console_scripts": [
            "metasnake=main:main"
        ]
    },
    classifiers=["Topic :: Scientific/Engineering :: Bio-Informatics"],
)

