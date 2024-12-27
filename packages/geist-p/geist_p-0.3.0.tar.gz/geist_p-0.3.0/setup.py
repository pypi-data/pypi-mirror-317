from setuptools import find_packages, setup

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="geist-p",
    version="0.3.0",
    description="Geist: a multimodal data transformation, query, and reporting language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cirss.github.io/geist-p/0.3/",
    author="Meng Li, Timothy McPhillips, Bertram Ludäscher",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["jinja2>=3.1.3", "jinja2-simple-tags>=0.5.0", "rdflib>=7.0.0", "owlrl>=6.0.2", "click>=8.1.7", "pyarrow>=15.0.0", "pandas>=2.2.0", "tabulate>=0.9.0", "pygraphviz>=1.12", "duckdb>=0.10"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
    entry_points='''
        [console_scripts]
        geist=geist.__main__:cli
    ''',
)
