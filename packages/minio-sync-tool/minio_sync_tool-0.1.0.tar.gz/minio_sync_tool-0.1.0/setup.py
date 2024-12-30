from setuptools import setup, find_packages

VERSION="0.1.0"

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="minio_sync_tool",
    version=VERSION,
    author="Nguyen Tran Trung",
    author_email="trungnt17@vng.com.vn",
    description="A package for synchronizing and uploading repositories with MinIO.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Use README.md as the description
    url="https://zalogit2.zing.vn/nlp/kilm/ai-platform/minio-sync-tool",
    packages=find_packages(where="src"),  # Find packages in the 'src' directory
    package_dir={"": "src"},  # Map source directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify Python version requirement
    install_requires=[
        "minio",  # Specify MinIO Python SDK version or range
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "minio_sync_tool=minio_sync_tool.cli:main",
        ],
    },
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
)
