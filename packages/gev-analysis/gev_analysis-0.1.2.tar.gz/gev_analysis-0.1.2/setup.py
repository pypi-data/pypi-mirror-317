from setuptools import setup, find_packages

setup(
    name="gev_analysis",
    version="0.1.2",
    description="A financial library for VaR and extreme value analysis",
    author="Tomasz Siatkowski",
    author_email="tomeksiat@gmail.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "yfinance"
    ],
    python_requires=">=3.8",
)
