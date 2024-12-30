from setuptools import setup, find_packages

setup(
    name="gev_analysis",
    version="0.3.0",
    description="A financial library for VaR and extreme value analysis",
    author="Tomasz Siatkowski",
    author_email="tomeksiat@gmail.com",
    license="MIT",
    packages=find_packages(where="src"),  # Automatyczne znajdowanie pakietów w katalogu src
    package_dir={"": "src"},  # Mapowanie głównego katalogu do src
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "yfinance"
    ],
    python_requires=">=3.8",
)
