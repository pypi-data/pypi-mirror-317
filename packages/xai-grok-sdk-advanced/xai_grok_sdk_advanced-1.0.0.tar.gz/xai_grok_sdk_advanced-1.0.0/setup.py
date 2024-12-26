from setuptools import setup, find_packages

setup(
    name="xai_grok_sdk_advanced",  # Name of the package
    version="1.0.0",  # Package version
    description="Advanced SDK for interacting with xAI Grok API",  # Short description
    long_description=open("README.md").read(),  # Long description from README.md
    long_description_content_type="text/markdown",  # Format of the long description
    author="Einstein Nsekele",  # Author's name
    author_email="einkap1@gmail.com",  # Author's email
    url="https://github.com/wealth0000110/xai_grok_sdk",  # URL for the project
    packages=find_packages(),  # Automatically find all packages
    install_requires=["requests"],  # Dependencies
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
        "Bug Tracker": "https://github.com/yourusername/xai_grok_sdk/issues",
        "Source Code": "https://github.com/yourusername/xai_grok_sdk",
        "Documentation": "https://github.com/yourusername/xai_grok_sdk/wiki",
    },
)
