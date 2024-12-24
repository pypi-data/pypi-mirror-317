from setuptools import setup, find_packages

setup(
    name="crypto_hell",
    version="0.1.4",                 # Update as needed
    packages=find_packages(),
    # If your package has any external dependencies, list them here.
    install_requires=[
        # 'requests>=2.25.1'
    ],
    author="Your Name",
    author_email="your_email@example.com",
    description="A sample package for crypto_hell",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
