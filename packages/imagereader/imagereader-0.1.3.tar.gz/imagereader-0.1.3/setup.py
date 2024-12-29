from setuptools import setup, find_packages

setup(
    name="imagereader",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        'openai>=1.0.0',
    ],
    author="Pedro Henrique Brito de Moraes",
    description="Biblioteca para análise de imagens usando OpenAI Vision",
    python_requires='>=3.6',
)