from setuptools import setup, find_packages


setup(
    name="logger_alionic",  # Replace with your library name (must be unique on PyPI)
    version="0.1.0",  # Semantic versioning: MAJOR.MINOR.PATCH
    author="alionic",
    author_email="alionic@example.com",
    description="",
    long_description="",  # Usually the contents of README.md
    long_description_content_type="text/markdown",  # Content type of your README
    url="",  # GitHub or project URL
    packages=find_packages(),  # Automatically find and include all packages in your project
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",  # Choose a license
    #     "Operating System :: OS Independent",
    # ],
    python_requires=">=3.6",  # Minimum Python version required
    install_requires=[
        "loguru",
        "psutil",
        "python-dotenv", 
    ],
    extras_require={
        "dev": ["pytest", "flake8"],  # Optional dependencies for development
    },
    # entry_points={
    #     "console_scripts": [
    #         "your-tool-name=your_package.module:function",  # Replace with your CLI entry point
    #     ],
    # },
    include_package_data=True,  # Include files listed in MANIFEST.in
    zip_safe=False,  # Set to False if the package includes non-Python files
)
