from setuptools import setup, find_packages

# Read the long description from the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="instacapture",
    version="0.2.0",
    author="Prathmesh Soni",
    author_email="info@soniprathmesh.com",
    description="A Python package for downloading Instagram stories, posts, reels, IGTV videos, and profile pictures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prathmeshsoni/InstaCapture",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pytz",
        "requests",
        "lxml"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    keywords="Instagram downloader stories reels posts",
)
