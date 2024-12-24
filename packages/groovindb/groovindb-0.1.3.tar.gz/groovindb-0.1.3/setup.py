from setuptools import setup, find_packages

setup(
    name="groovindb",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "questionary>=1.10.0",
        "asyncpg>=0.27.0",
        "aiomysql>=0.1.1",
        "colorama>=0.4.4",
        "redis>=5.0.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "groovindb=scripts.groovindb:cli",
        ],
    },
    author="Juan Manuel Panozzo Zenere",
    author_email="juan@groovinads.com",
    description="ORM asíncrono para Python con interfaz similar a Prisma",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/groovinads/groovindb",
    project_urls={
        "Bug Tracker": "https://bitbucket.org/groovinads/groovindb/issues",
        "Documentation": "https://bitbucket.org/groovinads/groovindb/src/main/README.md",
        "Source Code": "https://bitbucket.org/groovinads/groovindb",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
    ],
    python_requires=">=3.8",
) 