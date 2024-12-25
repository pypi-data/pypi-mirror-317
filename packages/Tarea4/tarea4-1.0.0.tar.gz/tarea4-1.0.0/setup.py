from setuptools import setup, find_packages

setup(
    name="Tarea4",  # Nombre único del paquete en PyPI
    version="1.0.0",  # Versión del paquete
    author="Alvaro Gomez Tejada",
    author_email="cresnik17021983@gmail.com",
    description="Gestión hotelera con soporte para reservas y administración de salones.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu_usuario/Tarea4",  # Enlace al repositorio (si tienes uno)
    packages=find_packages(),  # Detecta automáticamente todos los submódulos
    include_package_data=True,  # Incluye archivos como imágenes y SQL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Versión mínima de Python requerida
    install_requires=[
        # Lista las dependencias de requirements.txt
        "PySide6>=6.0.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
    ],
)
