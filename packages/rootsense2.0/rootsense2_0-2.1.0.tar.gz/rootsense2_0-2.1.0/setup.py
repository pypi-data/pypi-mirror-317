from setuptools import setup, find_packages

setup(
    name="rootsense2.0",
    version="2.1.0",
    description="A multithreading application for system monitoring and resource analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Amey Yarnalkar",
    author_email="yarnalkaramey@gmail.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pymongo",
        "streamlit",
        "scipy",
        "sklearn",
        "pandas",
        "numpy",
        "psutil",
        "time",
        "datetime",
        "logging",
        "argparse",
        "plotly",
        "os",  
        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "rootsense2=rootsense2.threading:main",
        ],
    },
)
