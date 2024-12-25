from setuptools import setup, find_packages

setup(
    name="wallet_fetcher",
    version="0.1.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="Fetch Solana wallet senders",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wallet_fetcher",  # Replace with your GitHub URL
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
