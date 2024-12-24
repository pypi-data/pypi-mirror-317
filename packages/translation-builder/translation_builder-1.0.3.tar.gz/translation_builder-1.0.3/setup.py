import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="translation-builder",
    author="Vadym Teliatnyk",
    author_email="laivhakin@gmail.com",
    description="A tool for generating Python classes from YAML files",
    keywords="package, translation, translator, komo4ek, convert, convertor, builder, translation-builder, translation-generator, g-translation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Komo4ekoI/translations-builder",
    project_urls={
        "Documentation": "https://github.com/Komo4ekoI/translations-builder",
        "Bug Reports": "https://github.com/Komo4ekoI/translations-builder/issues",
        "Source Code": "https://github.com/Komo4ekoI/translations-builder",
    },
    version="1.0.3",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "g-translation=translation_builder.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.8",
    install_requires=["PyYAML==6.0.2", "black==24.8.0"],
)
