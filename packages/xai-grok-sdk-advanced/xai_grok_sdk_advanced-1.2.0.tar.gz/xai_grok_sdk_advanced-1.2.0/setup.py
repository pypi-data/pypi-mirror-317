from setuptools import setup, find_packages

setup(
    name="xai_grok_sdk_advanced",  # Name of the package
    version="1.2.0",  # Updated version to reflect enhancements
    description="Advanced SDK for xAI Grok API with direct import, analytics, and rate-limit handling",
    license="MIT",  # Open-source license
    long_description=open("README.md").read() if "README.md" in open("MANIFEST.in").read() else "See project documentation for details.",
    long_description_content_type="text/markdown",  # Format of the long description
    author="Einstein Nsekele",  # Author's name
    author_email="einkap1@gmail.com",  # Author's email
    url="https://github.com/wealth0000110/xai_grok_sdk",  # URL for the project
    packages=find_packages(exclude=["tests*", "examples*", "*.tests"]),  # Automatically find all packages except test-related files
    py_modules=["XaiGrokSDK"],  # Include XaiGrokSDK.py as a top-level module
    include_package_data=True,  # Include additional files (e.g., LICENSE, README.md)
    install_requires=[
        "requests>=2.0,<3",  # Ensures compatibility with the correct version of requests
    ],
    extras_require={
        "dev": ["pytest", "requests-mock"],  # Additional packages for development
    },
    python_requires=">=3.7",  # Supported Python versions
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    project_urls={  # Additional URLs for the project
        "Bug Tracker": "https://github.com/wealth0000110/xai_grok_sdk/issues",
        "Source Code": "https://github.com/wealth0000110/xai_grok_sdk",
        "Documentation": "https://github.com/wealth0000110/xai_grok_sdk/wiki",
    },
    entry_points={
        "console_scripts": [
            "xai-grok-sdk = XaiGrokSDK:main",  # Example: Add an entry point for CLI if required
        ],
    },
)

