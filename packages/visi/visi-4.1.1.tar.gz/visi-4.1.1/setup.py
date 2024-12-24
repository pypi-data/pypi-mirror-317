from setuptools import setup, find_packages
import os

VERSION = "4.1.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="visi",
    description=("A CLI utility for Visi"),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Filip Dimitrovski",
    url="https://github.com/fikisipi/gpr",
    project_urls={
        # "Documentation": "https://llm.datasette.io/",
        # "Issues": "https://github.com/fikisipi/llm/issues",
        # "CI": "https://github.com/fikisipi/llm/actions",
        # "Changelog": "https://github.com/fikisipi/llm/releases",
    },
    license="Filip Dimitrovski",
    version=VERSION,
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        visi=visi.cli:cli
    """,
    install_requires=[
        "click",
        "openai>=1.0",
        "term-image==0.7.1",
        "uvicorn",
        "click-default-group>=1.2.3",
        # "sqlite-utils>=3.37",
        # "sqlite-migrate>=0.1a2",
        "pydantic>=1.10.2",
        "PyYAML",
        "pluggy",
        "python-ulid",
        "google-cloud-storage",
        "google-generativeai",
        "setuptools",
        "pip",
        "pyreadline3; sys_platform == 'win32'",
        "puremagic",
    ],
    extras_require={
        "test": [
            "pytest",
            "numpy",
            "pytest-httpx>=0.33.0",
            "pytest-asyncio",
            "cogapp",
            "mypy>=1.10.0",
            "black>=24.1.0",
            "ruff",
            "types-click",
            "types-PyYAML",
            "types-setuptools",
        ]
    },
    python_requires=">=3.9",
)
