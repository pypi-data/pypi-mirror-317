from setuptools import setup, find_packages

setup(
    name="proyecto-final-kraken",
    version="0.1.2",  # Cambia la versión para reflejar los cambios
    description="Un proyecto para calcular entradas de compra y venta usando las Bandas de Bollinger y la API de Kraken.",
    author="Pedro Montt Pacheco",
    author_email="p-montt@hotmail.com",
    url="https://github.com/pmontt/proyecto-kraken",  # Cambia esto por tu URL de GitHub
    packages=find_packages(where="."),  # Encuentra paquetes dentro de "./"
    package_dir={"": "."},  # Define "." como la raíz
    include_package_data=True,
    install_requires=[
        "krakenex==2.2.2",
        "matplotlib==3.10.0",
        "pandas==2.2.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "proyecto-python=proyecto_python.main:main",
        ],
    },
)
