from setuptools import setup, find_packages

setup(
    name="xlsxtofits",
    version="1.0.0",
    description="A Python package to convert XLSX files to FITS files.",
    author="xiangyunchuan",
    author_email="xiang_yunchuan@yeah.net",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "astropy",
        "openpyxl"
    ],
    entry_points={
        "console_scripts": [
            "xlsx-to-fits=xlsx_to_fits.cli:main",
        ],
    },
)