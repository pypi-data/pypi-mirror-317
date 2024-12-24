from setuptools import setup, find_packages
import os

# Leer el contenido del README
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Leer los requisitos
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="groovindb",
    version="0.1.0",
    description="ORM asíncrono con interfaz similar a Prisma para PostgreSQL y MySQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Juan Manuel Panozzo Zénere",
    author_email="juanmanuel.panozzo@groovinads.com",
    url="https://github.com/jmpanozzogroovinads/groovindb",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'groovindb=src.cli:cli',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="database orm async postgresql mysql prisma",
    project_urls={
        "Documentation": "https://github.com/jmpanozzogroovinads/groovindb/docs",
        "Source": "https://github.com/jmpanozzogroovinads/groovindb",
        "Tracker": "https://github.com/jmpanozzogroovinads/groovindb/issues",
    },
) 