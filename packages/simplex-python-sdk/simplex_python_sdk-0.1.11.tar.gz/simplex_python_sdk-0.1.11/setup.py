from setuptools import setup, find_packages

setup(
    name="simplex-python-sdk",
    version="0.1.11",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "tiktoken>=0.5.0",
        "click>=8.0.0",
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.0",
        "playwright>=1.0.0",
        "Pillow>=9.0.0",
    ],
    entry_points={
        'console_scripts': [
            'simplex=simplex.cli:main',
        ],
    },
    author="Simplex Labs, Inc.",
    author_email="founders@simplex.sh",
    description="Official Python SDK for Simplex API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shreyka/simplex-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
) 