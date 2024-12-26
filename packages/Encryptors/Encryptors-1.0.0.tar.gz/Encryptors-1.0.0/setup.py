from setuptools import setup, find_packages

setup(
    name="Encryptors",  # Nombre de la librería
    version="1.0.0",  # Versión inicial
    author="Anderson",
    author_email="andersito0016@gmail.com",
    description="Una librería de ejemplo en Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},  # Especifica que los paquetes están dentro de `src`
    packages=find_packages(where="src"),  # Encuentra todos los paquetes dentro de `src`
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # Versión mínima de Python
    install_requires=[
        "cryptography>=42.0.0",  # Declarar dependencias
    ],
    
)
