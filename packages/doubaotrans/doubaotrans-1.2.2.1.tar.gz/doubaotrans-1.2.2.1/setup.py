from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="doubaotrans",
    version="1.2.2.1",
    author="kilon",
    author_email="a15607467772@163.com", 
    description="A professional translation toolkit based on Doubao API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kilolonion/Doubaotranslator",  
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
        "httpx>=0.24.0",
        "openai>=1.0.0",
        "tenacity>=8.0.0",
        "python-dotenv>=0.19.0",
        "langdetect>=1.0.9",
        "requests>=2.25.0"
    ],
    extras_require={
        'http2': ["hyper>=0.7.0"],
        'dev': [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "mypy>=0.900"
        ]
    },
    package_data={
        'doubaotrans': ['py.typed', '*.pyi', '**/*.pyi'],
    },
    include_package_data=True,
) 