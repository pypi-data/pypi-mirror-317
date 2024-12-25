from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cryptobalancefinder",
    version="1.0.0",
    author="CryptoBalanceFinder Team",
    author_email="rbmorena42@gmail.com",
    description="A tool for finding and checking cryptocurrency wallet balances from seed phrases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cryptobalancefinder",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
        "pyyaml>=5.1",
        "bip_utils>=2.9.3",
        "argparse>=1.4.0",
    ],
    entry_points={
        'console_scripts': [
            'cryptobalancefinder=cryptobalancefinder.wallet_manager:main',
        ],
    },
    package_data={
        'cryptobalancefinder': ['bip39_wordlist.txt'],
    },
)
