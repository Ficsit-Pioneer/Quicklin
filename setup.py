"""Quicklin — Ultra-efficient shorthand that transpiles to Kotlin."""

from pathlib import Path

from setuptools import setup

# Read the long description from README.md
_HERE = Path(__file__).resolve().parent
_README = (_HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="quicklin",
    version="1.0.0",
    description="Ultra-efficient shorthand that transpiles to Kotlin",
    long_description=_README,
    long_description_content_type="text/markdown",
    author="Quicklin Contributors",
    author_email="quicklin@example.com",
    url="https://github.com/quicklin-lang/quicklin",
    project_urls={
        "Bug Tracker": "https://github.com/quicklin-lang/quicklin/issues",
        "Source Code": "https://github.com/quicklin-lang/quicklin",
        "Documentation": "https://github.com/quicklin-lang/quicklin#readme",
    },
    license="MIT",
    packages=["quicklin"],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "quicklin=quicklin.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Code Generators",
        "Operating System :: OS Independent",
    ],
    keywords=["kotlin", "transpiler", "shorthand", "quicklin", "code-generation"],
)
