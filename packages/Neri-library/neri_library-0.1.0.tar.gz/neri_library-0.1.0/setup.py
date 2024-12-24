from setuptools import setup, find_packages

setup(
    name="Neri_library",  # Nome do pacote
    version="0.1.0",  # Versão inicial
    author="Neri",  # Seu nome
    author_email="gui.neriaz@gmail.com",  # Seu e-mail
    description="Me segue no insta ae @_._neri",  # Descrição breve
    long_description_content_type="text/markdown",  # Formato da descrição longa
    packages=find_packages(),  # Localizar automaticamente subpacotes
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Versão mínima do Python
    install_requires=[  # Dependências do pacote
    "selenium",
    "selenium-stealth",
    "undetected-chromedriver",
    "requests",
    ],
)
