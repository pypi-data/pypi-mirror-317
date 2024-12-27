# mi_libreria/setup.py
from setuptools import setup, find_packages

setup(
    name="chasis_asa_microservices",  # Nombre del paquete para pip
    version="0.2.16",     # Versión inicial
    packages=find_packages(),
    install_requires=[],  # Lista de dependencias si las tienes
    author="Mikel",
    author_email="mikel.fernandezdelab@alumni.mondragon.edu",
    description="Librería de funciones genéricas en Python para microservicios",
    url="https://gitlab.com/asa-microservicios",  # URL del repositorio (si lo tienes)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
