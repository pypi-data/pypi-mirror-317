# File: setup.py
from setuptools import setup, find_packages

# Core requirements in setup.py
INSTALL_REQUIRES = [
    "click>=8.0.0",
    "pytest>=8.0.0",
]

def read_requirements(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Read README with proper encoding
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jformat",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,  # This is important for including non-Python files
    install_requires=INSTALL_REQUIRES,  
    #install_requires=read_requirements("requirements.txt"),
    extras_require={
        'dev': read_requirements('requirements-dev.txt'),
    },
    entry_points={
        "console_scripts": [
            "jformat=jformat.cli:main",
        ],
    },
    author="Soonwook Hwang",
    author_email="hwang@kisti.re.kr",
    description="A tool for formatting JSON files",
    #long_description=open("README.md").read(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hwang2006/jformat",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
