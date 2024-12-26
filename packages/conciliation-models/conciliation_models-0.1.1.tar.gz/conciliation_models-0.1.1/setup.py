from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="conciliation_models",
    version="0.1.1",
    description="Modelos y daos de la base de datos, para los proyectos de Servicios Adhoc y Airflow Conciliaciones",
    author="Conciliaciones - Kuantik",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.110.2",
        "pydantic>=2.7.1",
        "pymongo>=4.7.0",
        "inflect>=7.2.1",
        "boto3>=1.34.99",
        "boto3-stubs[s3]>=1.34.99",
        "loggerk>=0.0.5",
        "pandas>=2.2.2",
    ],
    python_requires=">=3.8",
)
