from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="itmgr",
    version="1.0.4",
    description=" An import manager that allow you to manage easily your importations in your project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Casssian/itmgr",
    author="Cassssian",
    author_email="enzod1604@gmail.com",
    entry_points={
        'console_scripts': [
            'itmgr=itmgr.itmgr:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Software Distribution",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ],

    keywords = "import, importations, development, package-manager, module-manager, dynamic-import, pip-wrapper, dependency-management, python-imports, import-automation, package-installer, module-installer, import-helper, development-tools, python-utilities, package-management, module-handling, import-handling, dependency-installer, python-modules, import-utilities",
    
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "pip>=21.0",
        "setuptools>=61.0",
        "wheel>=0.37.0",
        "typing-extensions>=4.0",
        "requests>=2.31.0",
        "packaging>=23.0"
    ],

    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "isort>=5.0",
            "mypy>=0.9",
            "pylint>=2.0",
            "flake8>=4.0"
        ],
        "test": ["pytest", "pytest-cov", "coverage"],
    },

    package_data={
        "itmgr": ["py.typed"],
    },
    project_urls={
        "Homepage" : "https://github.com/Cassssian/itmgr",
        "Bug Reports" : "https://github.com/Cassssian/itmgr",
        "Say Thanks!" : "https://github.com/Cassssian/itmgr",
        "Source" : "https://github.com/Cassssian/itmgr/",
        "Documentation" : "https://github.com/Cassssian/itmgr",
        "Changelog" : "https://github.com/Cassssian/itmgr",
        "Author" : "https://github.com/Cassssian",
        "Repository" : "https://github.com/Cassssian/itmgr.git",
        "Issues" : "https://github.com/Cassssian/itmgr/issues",
    },
)


