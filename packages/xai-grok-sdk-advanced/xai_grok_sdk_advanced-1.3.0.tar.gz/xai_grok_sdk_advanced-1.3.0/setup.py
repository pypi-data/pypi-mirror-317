from setuptools import setup, find_packages

setup(
    name="xai_grok_sdk_advanced",
    version="1.3.0",  # Updated version to reflect enhancements
    description="Advanced SDK for xAI Grok API with analytics and rate-limit handling",
    license="MIT",
    long_description=open("README.md").read() if "README.md" in open("MANIFEST.in").read() else "See project documentation for details.",
    long_description_content_type="text/markdown",
    author="Einstein Nsekele",
    author_email="einkap1@gmail.com",
    url="https://github.com/wealth0000110/xai_grok_sdk",
    packages=find_packages(exclude=["tests*", "examples*", "*.tests"]),
    py_modules=["XaiGrokSDK"],
    include_package_data=True,
    install_requires=[
        "requests>=2.0,<3"
    ],
    extras_require={
        "dev": ["pytest", "requests-mock"],
    },
    python_requires=">=3.7",
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
    project_urls={
        "Bug Tracker": "https://github.com/wealth0000110/xai_grok_sdk/issues",
        "Source Code": "https://github.com/wealth0000110/xai_grok_sdk",
        "Documentation": "https://github.com/wealth0000110/xai_grok_sdk/wiki",
    },
    entry_points={
        "console_scripts": [
            "xai-grok-sdk = XaiGrokSDK:main",
        ],
    },
)
