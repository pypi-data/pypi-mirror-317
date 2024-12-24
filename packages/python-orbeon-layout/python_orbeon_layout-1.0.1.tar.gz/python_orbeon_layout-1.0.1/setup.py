from setuptools import setup, find_packages


setup(
    name="python-orbeon-layout",
    version="1.0.1",
    packages=find_packages(),
    description="Uma biblioteca simples e independente para geração de layouts padronizados em formatos PDF e imagem.",
    author="Edu Fontes",
    author_email="eduramofo@gmail.com",
    url="https://github.com/getorbeon/python-orbeon-layout",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
