from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="timespacex",
    version="0.1.0",
    author="Hamed Yaghoobian",
    author_email="hamedyaghoobian@gmail.com",
    description="A Python Time and Space Complexity Analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hamedyaghoobian/timespacex",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="complexity analysis, big o notation, algorithm analysis, time complexity, space complexity",
    python_requires=">=3.6",
    install_requires=[
        "rich>=10.0.0"
    ],
    entry_points={
        'console_scripts': [
            'timespacex=timespacex.cli:main',
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/hamedyaghoobian/timespacex/issues",
        "Source": "https://github.com/hamedyaghoobian/timespacex",
    },
) 