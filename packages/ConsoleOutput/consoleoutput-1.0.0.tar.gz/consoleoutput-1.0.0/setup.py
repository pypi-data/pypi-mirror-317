from setuptools import setup, find_packages

setup(
    name="ConsoleOutput",
    version="1.0.0",
    author="Carlos-dev-G",
    author_email="baa4tsdev@gmail.com",
    description="Es una librería ligera y fácil de usar que permite aplicar estilos y colores a los textos que se imprimen en la consola",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Carlos-dev-G/ConsoleOutput",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)
